import os

from autogen import AssistantAgent
from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager


# 電気を付ける関数
# 電気を付けることに成功した場合はTrueを返す
def turn_on_the_light() -> bool:
    # ここにIoT機器を操作するAPI呼び出しを記述する
    print("call turn_on_the_light", "電気をつけました")
    return True


# エアコンを付ける関数
# エアコンを付けることに成功した場合はTrueを返す
def turn_on_the_air_conditioner() -> bool:
    # ここにIoT機器を操作するAPI呼び出しを記述する
    print("call turn_on_the_air_conditioner", "エアコンをつけました")
    return True


# デバイス管理エージェント
device_agent = ConversableAgent(
    name="DeviceAgent",
    system_message="""
    ## 指示
    あなたは室内のIoT機器を制御するAIです。
    ユーザの指示により、適切な機能を実行してください。
    最も適切な回答が完成したら、最後にTERMINATEと出力してください。
    """,
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# デバイスエージェントに関数を登録する
device_agent.register_for_llm(name="turn_on_the_light", description="電気を付ける関数")(turn_on_the_light)
device_agent.register_for_llm(name="turn_on_the_air_conditioner", description="エアコンを付ける関数")(
    turn_on_the_air_conditioner)


# 音楽のレコメンド
# 引数の雰囲気にあった曲名を返す
def recommend_music(feeling: str) -> str:
    # SpotifyのレコメンドAPIとかを呼べばいい
    print("call recommend_music", "楽曲提案をしました。")
    if feeling == "sad":
        return "レット・イット・ビー"
    elif feeling == "楽しい":
        return "天体観測"
    else:
        return "レモン"


# 音楽エージェント
music_agent = AssistantAgent(
    name="MusicAgent",
    system_message="""
    ## 指示
    あなたは音楽に詳しい人です。
    ユーザの気分に合わせたオススメの曲を提案してください。
    最も適切な回答が完成したら、最後にTERMINATEと出力してください。
    """,
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

music_agent.register_for_llm(name="recommend_music", description="ユーザの気分からオススメの楽曲を提案する関数")(recommend_music)


# ユーザ認証関数
def auth(password: str) -> bool:
    passwords = [
        "1111",
        "2222"
    ]
    if password in passwords:
        return True
    else:
        return False


# 認証エージェント
auth_agent = AssistantAgent(
    name="AuthAgent",
    system_message="""
    ## 指示
    あなたはユーザ認証AIです。
    認証が必要な機能の呼び出しを依頼された場合、必ずユーザ認証をしてください。
    ユーザ認証に失敗した場合、再度認証情報を確認してください。
    
    認証が必要な機能は以下です。
    * クーラーを付ける
    
    最も適切な回答が完成したら、最後にTERMINATEと出力してください。
    """,
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

auth_agent.register_for_llm(name="auth", description="パスワードを受け取り認証を行う関数")(auth)

# ユーザープロキシエージェントはアシスタントエージェントと対話するために使用されます。
# ツールコールを実行します。
user_proxy = AssistantAgent(
    name="Manager",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# ツール関数をユーザプロキシエージェントに登録します
user_proxy.register_for_execution(name="turn_on_the_light")(turn_on_the_light)
user_proxy.register_for_execution(name="turn_on_the_air_conditioner")(turn_on_the_air_conditioner)
user_proxy.register_for_execution(name="recommend_music")(recommend_music)
user_proxy.register_for_execution(name="auth")(auth)

group_chat = GroupChat(
    agents=[user_proxy, device_agent, music_agent, auth_agent], messages=[], max_round=10, speaker_selection_method="auto"
)
manager = GroupChatManager(groupchat=group_chat)
# user_proxy.initiate_chat(manager, message="今日は少し悲しい気分だよ。なにかおすすめの曲はない？")
user_proxy.initiate_chat(manager, message="クーラーつけて---")

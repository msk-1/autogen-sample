import os

from autogen import ConversableAgent
from autogen import AssistantAgent
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


agent1 = ConversableAgent(
    name="Agent1",
    system_message="""
    ## 指示
    ユーザから電話番号を聞いて下さい。
    電話番号が確認できたら、最後にTERMINATEと出力してください。
    """,
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
)

# デバイスエージェントに関数を登録する
agent1.register_for_llm(name="turn_on_the_air_conditioner", description="エアコンを付ける関数")(
    turn_on_the_air_conditioner)

# 音楽エージェント
agent2 = AssistantAgent(
    name="Agent2",
    system_message="""
    ## 指示
    ユーザの氏名を確認してください。
    氏名が確認できたら、最後にTERMINATEと出力してください。
    """,
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
)

# ユーザープロキシエージェントはアシスタントエージェントと対話するために使用されます。
# ツールコールを実行します。
user_proxy = AssistantAgent(
    name="Manager",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="ALWAYS",
)

# ツール関数をユーザプロキシエージェントに登録します
user_proxy.register_for_execution(name="turn_on_the_light")(turn_on_the_light)
user_proxy.register_for_execution(name="turn_on_the_air_conditioner")(turn_on_the_air_conditioner)

group_chat = GroupChat(
    agents=[user_proxy, agent1, agent2], messages=[], max_round=20, speaker_selection_method="auto"
)
manager = GroupChatManager(groupchat=group_chat)
# user_proxy.initiate_chat(manager, message="今日は少し悲しい気分だよ。なにかおすすめの曲はない？")
user_proxy.initiate_chat(manager, message="こんにちは")

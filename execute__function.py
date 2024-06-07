import os
from typing import Annotated, Literal

from autogen import ConversableAgent
from autogen import GroupChat
from autogen import GroupChatManager

Operator = Literal["+", "-", "*", "/"]



def classification(input: str) -> str:
    print('input', input)
    if 'LDA' in input or 'イグニッション' in input:
        return 'マニュアル質問'
    elif '腹減った' in input or 'こんにちは' in input:
        return '雑談'
    elif '天気' in input:
        return '天気予報'

def get_weather(place: str) -> str:
    print(place)
    return place + '晴れ'

def get_manual_answer(question: str) -> str:
    return 'レーンディパーチャーアラートだよ'

# ツールコールを提案するアシスタントエージェントを定義しよう。
assistant_1 = ConversableAgent(
    name="Assistant1",
    system_message="""
    あなたは自動車に搭載されているアシスタントAIです。
    ユーザからの「雑談」、「依頼」、「質問」に対して、ユーザが満足するような完璧な応対をしてください。
    
    ユーザの入力は、以下に分類されます。入力内容を分類するために、分類関数が使用できます。
    ・雑談
    ・天気予報機能
    ・マニュアル質問
    
    分類関数の結果を踏まえ、適切な関数を呼び出して必要な情報を取得してください。
    関数に必要なパラメータが不足している場合はユーザに確認してください。
    
    最も適切な回答が完成したら、最後にTERMINATEと出力してください。
    """,
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# ツールコールを提案するアシスタントエージェントを定義しよう。
assistant_2 = ConversableAgent(
    name="Assistant2",
    system_message="""
    あなたは堅苦しい会話を明るく変換してくれるAIです。
    アシスタントAIが作成した堅苦しい応答内容を明るく元気な内容に変換してください。
    最も適切な回答が完成したら、最後にTERMINATEと出力してください。
    """,
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# ユーザープロキシエージェントはアシスタントエージェントと対話するために使用されます。
# ツールコールを実行します。
user_proxy = ConversableAgent(
    name="Manager",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# アシスタントエージェントにツールを登録する。
assistant_1.register_for_llm(name="classification", description="入力内容を「雑談」、「マニュアル質問」、「天気予報」に分類します")(classification)
assistant_1.register_for_llm(name="get_weather", description="指定された場所の天気を返却します")(get_weather)
assistant_1.register_for_llm(name="get_manual_answer", description="マニュアルに関する質問への回答を返却します")(get_manual_answer)

# ツール関数をユーザプロキシエージェントに登録します
user_proxy.register_for_execution(name="classification")(classification)
user_proxy.register_for_execution(name="get_weather")(get_weather)
user_proxy.register_for_execution(name="get_manual_answer")(get_manual_answer)

groupchat = GroupChat(
    agents=[user_proxy, assistant_1, assistant_2], messages=[], max_round=10
)
manager = GroupChatManager(groupchat=groupchat)
user_proxy.initiate_chat(manager, message="""
user: こんにちは
assistant: こんにちは！
user: LDAってなに？
assistant: LDAは「レーン・ディパーチャー・アラート」の略です。車線を逸脱した場合に警告を発し、安全運転を支援するシステムです。
user: どうやって使うの？
assistant: カスタマイズメニューから設定するよ
user: いま東京にいる
assistant: 東京ですか！何をしていますか？
user: 今日の天気は？
""")

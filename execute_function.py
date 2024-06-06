import os
from typing import Annotated, Literal

from autogen import ConversableAgent

Operator = Literal["+", "-", "*", "/"]


def calculator(a: int, b: int, operator: Annotated[Operator, "operator"]) -> int:
    if operator == "+":
        return a + b
    elif operator == "-":
        return a - b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return int(a / b)
    else:
        raise ValueError("Invalid operator")


# ツールコールを提案するアシスタントエージェントを定義しよう。
assistant = ConversableAgent(
    name="Assistant",
    system_message="あなたは役に立つAIアシスタントだ。 "
                   "簡単な計算なら手伝えるだろう。 "
                   "すべてのタスクが完了したら、最後にTERMINATEと出力してください。",
    llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
)

# ユーザープロキシエージェントはアシスタントエージェントと対話するために使用されます。
# ツールコールを実行します。
user_proxy = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

# アシスタントエージェントにツールを登録する。
assistant.register_for_llm(name="calculator", description="A simple calculator")(calculator)

# ツール関数をユーザプロキシエージェントに登録します
user_proxy.register_for_execution(name="calculator")(calculator)

# 以下のようにまとめて登録も可能
# register_function(
#     calculator,
#     caller=assistant,  # The assistant agent can suggest calls to the calculator.
#     executor=user_proxy,  # The user proxy agent can execute the calculator calls.
#     name="calculator",  # By default, the function name is used as the tool name.
#     description="A simple calculator",  # A description of the tool.
# )

chat_result = user_proxy.initiate_chat(assistant, message="(100 + 20 / (10 - 5))は？")

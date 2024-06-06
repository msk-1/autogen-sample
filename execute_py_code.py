import logging
import os

from autogen import AssistantAgent, UserProxyAgent, config_list_from_json
from autogen.agentchat.contrib.gpt_assistant_agent import GPTAssistantAgent

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

assistant_id = os.environ.get("ASSISTANT_ID", None)

llm_config = {
    "config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}],
}

assistant_config = {"assistant_id": assistant_id}

SYSTEM_PROMPT = """
あなたはプログラマのアシスタントです。
プログラマの指示に従い、pythonのプログラムを作成し、プログラマに提出してください。

提出したプログラムをプログラマが実行した際、エラーが出た場合は修正して、再度プログラムを提出してください。
必ず、部分的なコードではなく、実行可能な完全なコードを提出してください。

すべてのタスクが完了したら、最後にTERMINATEと出力してください。
"""

gpt_assistant = GPTAssistantAgent(
    name="assistant",
    instructions=SYSTEM_PROMPT,
    llm_config=llm_config,
    assistant_config=assistant_config,
)

user_proxy = UserProxyAgent(
    name="user_proxy",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    is_termination_msg=lambda msg: "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
    max_consecutive_auto_reply=1,
)
user_proxy.initiate_chat(gpt_assistant, message="hello worldと出力する")

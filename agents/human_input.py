from autogen import ConversableAgent


class HumanInput:
    def __init__(self):
        # ユーザ入力介入
        self.human_proxy = ConversableAgent(
            "human_proxy",
            llm_config=False,  # no LLM used for human proxy
            human_input_mode="ALWAYS",  # always ask for human input
            is_termination_msg=lambda msg: msg.get("content") is not None and (
                    "FINISH" in msg["content"].upper())
        )

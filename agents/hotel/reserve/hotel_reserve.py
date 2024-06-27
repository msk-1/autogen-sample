from autogen import AssistantAgent

from hotel import reserve_hotel


class HotelReserve:

    def __init__(self, llm_config):
        # ホテル予約エージェント
        self.hotel_reserve_agent = AssistantAgent(
            name="HotelReserveAgent",
            system_message="""
            ## 指示
            あなたはホテルの予約アシスタントです。
            ユーザから指定されたホテルを予約してください。
    
            ## 制約事項
            * ホテルを予約する前に、ホテルを予約してよいかユーザに確認し、承諾が得られた場合のみホテルを予約してください
            * ホテルの予約が完了した場合: next suggestionと出力してください
            """,
            # llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
            llm_config=llm_config,
            is_termination_msg=lambda msg: msg.get("content") is not None and (
                    "FINISH" in msg["content"].upper())
            ,
            human_input_mode="TERMINATE",
        )

        self.hotel_reserve_agent.register_for_llm(name="reserve_hotel", description="指定されたホテル名のホテルを予約する")(
            reserve_hotel)

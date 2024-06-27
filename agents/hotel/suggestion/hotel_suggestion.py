
from autogen import AssistantAgent

from agents.hotel.suggestion.function import SUGGESTION_SPOT_FUNC_NAME
from hotel import reserve_hotel


class HotelSuggestion:
    def __init__(self, llm_config):
        # スポット提案エージェント
        self.hotel_reserve_agent = AssistantAgent(
            name="HotelSuggestionAgent",
            system_message="""
            ## 指示
            あなたはおすすめホテル周辺のスポットを提案するアシスタントです。
            ユーザが宿泊するホテル周辺のオススメスポットを提案してください。
    
            ## 制約事項
            * おすすめスポットの提案が完了した場合: next suggestionと出力してください
            """,
            # llm_config={"config_list": [{"model": "gpt-4o-2024-05-13", "api_key": os.environ["OPENAI_API_KEY"]}]},
            llm_config=llm_config,
            is_termination_msg=lambda msg: msg.get("content") is not None and (
                    "FINISH" in msg["content"].upper())
            ,
            human_input_mode="TERMINATE",
        )

        self.hotel_reserve_agent.register_for_llm(name=SUGGESTION_SPOT_FUNC_NAME, description="指定されたホテル名のホテルを予約する")(
            reserve_hotel)

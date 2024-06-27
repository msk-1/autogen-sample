from typing import Annotated

SUGGESTION_SPOT_FUNC_NAME = "suggestion_spot"

def search_hotel(hotel_name: Annotated[str, "ホテル名"]) -> str:
    if hotel_name == "東京":
        return "東京タワー"
    elif hotel_name == "神奈川":
        return "中華街"
    elif hotel_name == "千葉":
        return "ディズニーランド"
    else:
        return "富士山"

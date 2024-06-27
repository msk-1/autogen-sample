# ホテル検索
from datetime import datetime
from typing import Annotated

SEARCH_HOTEL_FUNC_NAME = "search_hotel"


def search_hotel(self, place: Annotated[str, "場所"], checkin_date: Annotated[datetime, "チェックイン日"],
                 checkout_date: Annotated[datetime, "チェックアウト日"], adult_number: Annotated[int, "宿泊者数"]) -> list:
    if place == "東京":
        return ["東京第1ホテル", "東京第2ホテル", "東京第3ホテル"]
    elif place == "神奈川":
        return ["神奈川第1ホテル", "神奈川第2ホテル", "神奈川第3ホテル"]
    elif place == "千葉":
        return ["千葉第1ホテル", "千葉第2ホテル", "千葉第3ホテル"]
    else:
        return ["第1ホテル", "第2ホテル", "第3ホテル"]

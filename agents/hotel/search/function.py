# ホテル検索
from datetime import datetime
from typing import Annotated


def search_hotel(self, place: Annotated[str, "場所"], checkin_date: Annotated[datetime, "チェックイン日"],
                 checkout_date: Annotated[datetime, "チェックアウト日"], adult_number: Annotated[int, "宿泊者数"]) -> list:
    if place == "群馬":
        return ["群馬第1ホテル", "群馬第2ホテル", "群馬第3ホテル"]
    elif place == "":
        return ["東京第1ホテル", "東京第2ホテル", "東京第3ホテル"]
    else:
        return ["三重第1ホテル", "三重第2ホテル", "三重第3ホテル"]

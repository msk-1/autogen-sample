import autogen

from agents.hotel.reserve.hotel_reserve import HotelReserve
from agents.hotel.search.hotel_search import HotelSearch
from agents.human_input import HumanInput

# LLM settings

config_list = autogen.config_list_from_json(
    "OAI_CONFIG_LIST",
    file_location="./",
    filter_dict={
        "model": ["geepeetee-four-turbo"],
    },
)

llm_config = {
    "config_list": config_list,
    "timeout": 120,
    "temperature": 0,
}

hotel_search = HotelSearch(llm_config)
hotel_search_agent = hotel_search.hotel_search_agent

hotel_reserve = HotelReserve(llm_config)
hotel_reserve_agent = hotel_reserve.hotel_reserve_agent

human_input = HumanInput()
human_proxy = human_input.human_proxy
human_proxy.register_for_execution(name="search_hotel")(hotel_search_agent.search_hotel)
human_proxy.register_for_execution(name="reserve_hotel")(hotel_reserve_agent.reserve_hotel)

initializer = autogen.UserProxyAgent(
    name="Init",
    code_execution_config=False,
)

speaker_hist = []


# 次のスピーカを選択する
def speaker_selection(last_speaker, groupchat):
    messages = groupchat.messages

    speaker_hist.append(last_speaker)

    if last_speaker is initializer:
        next_agent = hotel_search_agent
    elif last_speaker is hotel_search_agent:
        if "next reserve" in messages[-1]["content"]:
            # エージェントの発話にnext reserveが含まれる場合、ホテル予約エージェントを指定
            next_agent = hotel_reserve_agent
        else:
            # それ以外の場合、ユーザ入力を指定
            next_agent = human_proxy
    elif last_speaker is hotel_reserve_agent:
        next_agent = human_proxy
    else:
        # 最後のスピーカーがhumanの場合、前回のスピーカーを指定
        next_agent = speaker_hist[-2]
    return next_agent


groupchat = autogen.GroupChat(
    agents=[initializer, human_proxy, hotel_reserve_agent, hotel_search_agent],
    messages=[],
    max_round=20,
    speaker_selection_method=speaker_selection,
)
manager = autogen.GroupChatManager(groupchat=groupchat)

initializer.initiate_chat(
    manager, message="こんにちは"
)

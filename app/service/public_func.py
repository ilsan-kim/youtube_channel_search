from functools import reduce

import googleapiclient.discovery


def check_items_length(total_result: int):
    if total_result == 0:
        raise ValueError("No More Search Results")
    elif total_result > 0:
        pass


def check_subscriber_count(min_subscriber: int, max_subscriber: int, subscriber_count: int):
    if min_subscriber <= subscriber_count <= max_subscriber:
        print('subscriber : ', subscriber_count)
        return True
    else:
        return False


def get_next_page_token(response):
    try:
        next_page_token = response['nextPageToken']
    except:
        next_page_token = None
    return next_page_token


def get_channel_metadata(min_subscriber: int, max_subscriber: int, items: list, container: list):
    # 채널 정보 확인
    for item in items:
        # 채널 이름, 아이디, 썸네일
        channel_title = item['snippet']['title']
        channel_id = item['id']
        thumbnail_url = item['snippet']['thumbnails']['default']['url']

        # 구독자 확인
        try:
            subscriber_count = int(item['statistics']['subscriberCount'])
        except KeyError:
            subscriber_count = 0
        if check_subscriber_count(
                max_subscriber=max_subscriber,min_subscriber=min_subscriber,subscriber_count=subscriber_count) is False:
            print("No matches with coverage of subscribers Channel id : {}".format(channel_id))
            continue

        # 권역
        try:
            country = item['snippet']['country']
        except KeyError:
            country = "알 수 없음"

        # 기타 메타데이터
        avg_view = 0
        loyalty_rate = 0
        engagement_rate = 0

        item_detail = {
            "channel_title": channel_title,
            "thumbnail_url": thumbnail_url,
            "country": country,
            "subscriber_count": subscriber_count
        }
        container.append(item_detail)
    return container


def get_id_list(keyword: str, region_code: str, developer_key: str, page_token: str, type: str, container: list):
    youtube_api_client = googleapiclient.discovery.build('youtube', 'v3', developerKey=developer_key)
    channel_search_query = youtube_api_client.search().list(
        part='snippet',
        q=keyword,
        regionCode=region_code,
        type=type,
        maxResults=50,
        pageToken=page_token
    )
    response = channel_search_query.execute()

    # 검색 결과가 없을경우
    total_result = response["pageInfo"]["totalResults"]
    check_items_length(total_result=total_result)
    print("Total Searched Results : ", total_result)

    # 페이지 토큰 추출
    next_page_token = get_next_page_token(response=response)

    searched_items = [container.append(item['snippet']['channelId']) for item in response['items']]
    return {"type": type,"next_page_token": next_page_token, "searched_items": searched_items}


def get_channel_details(min_subscriber: int, max_subscriber: int, developer_key: str,
                       channel_ids_container: list, metadata_container: list):
    # 채널 아이디 검색하기 위해 str로 변환
    ids = reduce(lambda x, y: x + ', ' + y, channel_ids_container)

    # 유튜브 API 연결
    youtube_api_client = googleapiclient.discovery.build('youtube', 'v3', developerKey=developer_key)
    channel_search_query = youtube_api_client.channels().list(
        part='snippet, statistics',
        id=ids,
        maxResults=50
    )
    response = channel_search_query.execute()

    channel_meatadata = get_channel_metadata(
        items=response['items'], min_subscriber=min_subscriber, max_subscriber=max_subscriber, container=metadata_container
    )
    return {"searched_items": channel_meatadata}

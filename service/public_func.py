import googleapiclient.discovery


def check_items_length(total_result: int):
    if total_result == 0:
        raise ValueError("No More Search Results")
    elif total_result > 0:
        pass


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

    # 다음 검색 결과 확인
    try:
        next_page_token = response['nextPageToken']
    except KeyError:
        next_page_token = None

    searched_items = [container.append(item['snippet']['channelId']) for item in response['items']]
    return {"type": type,"next_page_token": next_page_token, "searched_items": searched_items}

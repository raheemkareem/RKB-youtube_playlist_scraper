import requests

API_KEY = '**ADD YOUR OWN API KEY HERE**'
PLAYLIST_ID = 'PLgiVKcoMxbtBfCO-wwH0VPw7OveM3gVL_'
BASE_URL = 'https://www.googleapis.com/youtube/v3'

def get_video_ids_from_playlist(playlist_id, api_key):
    video_ids = []
    url = f'{BASE_URL}/playlistItems'
    params = {
        'part': 'snippet',
        'playlistId': playlist_id,
        'maxResults': 50,
        'key': api_key
    }
    
    while True:
        response = requests.get(url, params=params)
        data = response.json()

        for item in data.get('items', []):
            video_id = item['snippet']['resourceId']['videoId']
            video_ids.append(video_id)
        
        if 'nextPageToken' in data:
            params['pageToken'] = data['nextPageToken']
        else:
            break

    return video_ids

def get_video_descriptions(video_ids, api_key):
    descriptions = []
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i:i+50]
        url = f'{BASE_URL}/videos'
        params = {
            'part': 'snippet',
            'id': ','.join(batch),
            'key': api_key
        }
        response = requests.get(url, params=params)
        data = response.json()
        for item in data.get('items', []):
            descriptions.append({
                'title': item['snippet']['title'],
                'description': item['snippet']['description']
            })
    return descriptions

# --- MAIN ---
video_ids = get_video_ids_from_playlist(PLAYLIST_ID, API_KEY)
descriptions = get_video_descriptions(video_ids, API_KEY)

for i, video in enumerate(descriptions, 1):
    print(f"{i}. {video['title']}\n{video['description']}\n{'-'*60}")

import json
import requests

def get_posts():

    # Searches for posts with certain tags and saves in a json file

    url = 'https://danbooru.donmai.us/posts.json?tags=limit:200+-taguel+panne_(fire_emblem)'
    response = requests.get(url)
    response_json = response.json()

    with open('danbooru_response2.json', 'w') as file:
        json.dump(response_json, file)''

def get_ids():

    # Opens json file and gets the ids

    with open('danbooru_response2.json', 'r') as json_data:
        jason = json.load(json_data)

    ids = []
    for index, dan_id in enumerate(jason):
        ids.append(jason[index]['id'])

    print(ids)
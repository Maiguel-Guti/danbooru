import json
import requests


def get_posts(tags: str, file_path: str) -> None:

    # Searches for posts with certain tags and saves in a json file

    url = 'https://danbooru.donmai.us/posts.json?tags={0}'.format(tags)
    response = requests.get(url)
    response_json = response.json()

    with open(file_path, 'w') as file:
        json.dump(response_json, file)


def get_ids(file_path: str) -> list:

    # Opens json file and gets the ids

    with open(file_path, 'r') as json_data:
        jason = json.load(json_data)

    ids = []
    for index, dan_id in enumerate(jason): ids.append(jason[index]['id'])
    ids.sort()

    return ids


def remove_ids(ids: list[int], ids_to_remove: list[int]) -> list[int]:
    for k in ids_to_remove:ids.remove(k)
    return ids


def main(tags: str, file_path: str, ids_to_remove: list[int] = None) -> list[int]:
    get_posts(tags, file_path)
    output = remove_ids(get_ids(file_path), ids_to_remove)
    print(len(output), ' ids')
    return output


if __name__ == '__main__':
    TAGS = 'limit:200+-taguel+yarne_(fire_emblem)'
    FILE_PATH = 'danbooru_response2.json'
    IDS_TO_REMOVE = [6037679, 1865322]
    print(main(tags=TAGS, file_path=FILE_PATH, ids_to_remove=IDS_TO_REMOVE))
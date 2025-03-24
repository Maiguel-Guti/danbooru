'''
Autor: maiguel
El proposito de este codigo es tomar una lista de IDs de pixiv
(que pueden estar en archivos locales) y revisar si ya se han
posteado en Danbooru.
La lista de IDs debe provenir de un objeto iterable, como una
lista o tupla y debe tener valores de tipo entero.
'''

import json
import requests

def response_counter(danbooru_json):
    # Cuenta la cantidad de posts que han sido aprovados y borrados de una misma ID de pixiv
    # en Danbooru. No cuenta flagged posts ni pendientes
    
    counter = {}
    size = len(danbooru_json)
    approved = 0
    deleted = 0
    danbooru_ids = []

    for post in range(size):
        danbooru_ids.append(danbooru_json[post]['id']) 
        if danbooru_json[post]['is_deleted']: deleted += 1
        else: approved += 1

    counter['posts'] = size
    counter['approved'] = approved
    counter['deleted'] = deleted
    counter['artist'] = danbooru_json[0]['tag_string_artist']
    counter['danbooru_ids'] = danbooru_ids

    return counter

def url_basic_generator(LIMIT_SEARCH: int, TEST:bool) -> str:

    if TEST: url = 'https://testbooru.donmai.us/posts.json?tags=limit:'+ str(LIMIT_SEARCH) + '+'
    else: url = 'https://danbooru.donmai.us/posts.json?tags=limit:'+ str(LIMIT_SEARCH) + '+'

    return url

def pixiv_status(client, pixiv_id: int):

    return 0

def main(pixiv_ids, max_checks: int = 200, limit_search: int = 20, test:bool = False):

    response_list = {}
    on_danbooru = {}
    not_found = []
    url = url_basic_generator(LIMIT_SEARCH=limit_search, TEST=test)

    # pixiv api

    print('Checking ', len(pixiv_ids), ' pixiv ids in', url[8:17])
    
    for index, pixiv_id in enumerate(pixiv_ids):
        
        if index >= max_checks:
            print('Max checks reached (', max_checks, ')') 
            break

        try: pixiv_id = int(pixiv_id)
        except:
            print('Error: not a valid ID, ', pixiv_id)
            continue


        pixiv_id_url = url + 'pixiv:' + str(pixiv_id)
        print(index+1, ' | ', round(100*index/len(pixiv_ids), 2),'% -', pixiv_id_url)
        response = requests.get(pixiv_id_url)
        response_json = response.json()
        
        # Si la busqueda no existe regresa lista vacia []
        if response_json != []: 
            on_danbooru[str(pixiv_id)] = response_counter(response_json)
        else: 
            not_found.append(pixiv_id) 

    response_list['not_in_danbooru'] = not_found
    response_list['uploaded'] = on_danbooru
    # response_list['partially_in_danbooru'] = not_found

    with open('pixiv_check.json', 'w') as file:
        json.dump(response_list, file)
   
    return 0

if __name__ == '__main__':
    print('---------------------')
    import get_pixiv_ids
    folder = r'C:\Users\Usuario\Desktop\WaraWara\pixiv\Estrellas'
    pixiv_ids = get_pixiv_ids.main(folder)
    main(pixiv_ids, test = True, max_checks = 2, limit_search=64)
    print('---------------------')
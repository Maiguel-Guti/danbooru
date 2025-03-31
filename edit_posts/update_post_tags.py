import requests

def create_auth() -> tuple:

    from os import environ

    username = 'Maiguel'
    api_key = environ['API_KEY_DANBOORU_UPDATE']
    login_args = (username, api_key)

    return login_args


def main(rating: str = None, tags: str = None, post_ids: list = None, login_args: tuple[str] = None) -> None:

    client = requests.Session() # Inicia una sesion persistente

    if rating != None: rating = str.lower(rating)

    payload =  {
                'post[rating]': rating, 
                'post[tag_string]': tags, # String. New tags added, use '-' to remove tags
                'post[old_tag_string]': '' # This ensures to keep previous tags
               }

    for index, post_id in enumerate(post_ids):
        url = 'https://danbooru.donmai.us/posts/{0}.json'.format(post_id) # reemplaza {0} con el post_id formateado como str
        response = client.put(url, data = payload, auth = login_args)

        print(
            round((index+1)*100/len(post_ids), 1), '% ', 
            url, '- Response: ', response.status_code
            )
    
    #test = requests.put(url='https://danbooru.donmai.us/posts/{0}.json?post[rating]=g'.format(post_id), auth=login_args)
    
    return


if __name__ == '__main__':

    LOGIN_ARGS = create_auth()
    
    import filtrar_historial as fhl
    archivo = r'C:\Users\Usuario\Desktop\Programacion\Python\Online\danbooru_resources\historial\BrowserHistory.csv'
    dia = (2025, 3, 29)
    AFTER_DATE = fhl.create_date_string(dia, (16, 17))
    BEFORE_DATE = fhl.create_date_string(dia, (23, 59, 59))
    ids = fhl.main(archivo, after_date=AFTER_DATE, before_date=None)
    ids = sorted(list(ids), reverse= True)
    ids =  [1284632, 1349676]  
    print(ids)

    main(tags='taguel', post_ids = ids, login_args = LOGIN_ARGS)
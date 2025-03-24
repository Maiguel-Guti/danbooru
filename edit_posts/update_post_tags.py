import requests

def create_auth() -> tuple:

    from os import environ

    username = 'Maiguel'
    api_key = environ['API_KEY_DANBOORU_UPDATE']
    login_args = (username, api_key)

    return login_args

def check_rating() -> bool:
    pass

def main(rating: str = None, tags: str = None, post_ids: list = None, login_args: tuple[str] = None) -> None:

    client = requests.Session() # Inicia una sesion persistente
    
    check_rating()

    payload =  {
        'post[rating]': rating, 
        'post[tag_string]': tags
               }

    for post_id in post_ids:
        url = 'https://danbooru.donmai.us/posts/{0}.json'.format(post_id) # reemplaza {0} con el post_id formateado como str
        response = client.put(url, data = payload, auth = login_args)

        print(url, '- Response: ', response.status_code)
    
    #test = requests.put(url='https://danbooru.donmai.us/posts/{0}.json?post[rating]=g'.format(post_id), auth=login_args)
    
    return


if __name__ == '__main__':

    LOGIN_ARGS = create_auth()
    ids = [29954, 29937, 29924]
    main('G', posts_ids = ids, login_args = LOGIN_ARGS)
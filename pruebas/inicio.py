import requests
import json

def main(url):
    response = requests.get(url)
    tabla = response.json()

    # Guarda la respuesta 'w' es para writing (sobreescribir)
    with open('danbooru_response.json', 'w') as file:
        json.dump(tabla, file) #.dumps??

    jason('danbooru_response.json')

    return tabla

def jason(arch):
    with open(arch, 'r') as file:
        # Al abrir un archivo json, hay que decirle a Python que lo cargue como json
        data = json.load(file) 
    print(data[0]['id'])


if __name__ == '__main__':
    print('----------------------')
    main(r'https://danbooru.donmai.us/posts.json?tags=pixiv:61469778')
    print('----------------------')                                                                                                                                                                                             



# link = 'https://danbooru.donmai.us/posts.json?tags=2boys rating:g&limit=1000&page=10'     
# r'https://testbooru.donmai.us/posts.json?tags=happy'
# r'https://testbooru.donmai.us/posts.json?tags=pixiv:61469778'                                                                                                  
'''


https://github.com/LuqueDaniel/pybooru/tree/master



If you have an alternate Danbooru address you would like to connect to, you also specify that in this string.

const booru = new Danbooru('http://safebooru.donmai.us/')

const login = 'login'
const key = 'api_key'

const authenticatedBooru = new Danbooru(
  `https://${login}:${key}@sonohara.donmai.us`
)

https://github.com/stawberri/danbooru-node

-------- METODO .Session() para conexion persistente y acelerar el codigo

https://stackoverflow.com/questions/32986228/difference-between-using-requests-get-and-requests-session-get



esto servira?????

prueba = requests.request('PUT', url,  auth=(username, api_key))
o
prueba = requests.put(url, auth=(username, api_key))

'''

import requests
api_key = 'VsEwmJzMyWyNDbmdjYPJRkxU'
username = 'Maiguel'

'Cambia el rating de un post de Danbooru'
test = requests.put(
    url='https://danbooru.donmai.us/posts/5021009.json?api_key='+ api_key +'&login=Maiguel&post[rating]=g'
    )
print(test)
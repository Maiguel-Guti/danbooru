'''
Autor: maiguel
Este codigo toma los archivos de una carpeta con imagenes de pixiv y guarda
las IDs de pixiv como lista en un archivo json.
'''

from os import listdir
import json

def main(folder: str, create_json: bool=False):
    raw_data = listdir(folder)
    clean_data = set() # Set es un conjunto que no acepta valores duplicados

    # Obtiene IDs del nombre de cada archivo
    for image in raw_data: 
        pixiv_id = get_id(image)
        if pixiv_id is not None: clean_data.add(pixiv_id)

    clean_data = list(clean_data)

    if create_json:
        with open('pixiv_ids.json', 'w') as f:
            json.dump(clean_data, f)

    return clean_data


def get_id(pixiv_filename: str):

    if pixiv_filename[:7] == 'illust_': 
        temp = pixiv_filename[7:]
        digitos = temp.find('_') # Algunas IDs tienen mas digitos que otras
        return temp[:digitos]
    
    else: return None


def get_date(pixiv_filename: str):
    # Pixiv almacena la hora y fecha de descarga del archivo en su nombre
    if pixiv_filename[:7] == 'illust_': 
        time = pixiv_filename[-10:-4]
        date = pixiv_filename[-19:-11]
        #date_time = datetime(
        #    year=int(date[:4]), month=int(date[4:6]), day=int(date[-2:]), hour=int(time[:2]), minute=int(time[2:4]), second=int(time[-2:])
        #                )
        return date, time
    
    else: return


if __name__ == '__main__':
    print('----------------')
    folder = r'C:\Users\Usuario\Desktop\WaraWara\pixiv\Estrellas'
    main(folder, True)
    print('----------------')
from classes import *
import os

if __name__ == '__main__':
    vk_id = input('Введите айди странички вк: ')
    ya_token = input('Токен яндекса: ')
    access_token = input('Токен ВК: ')
    vk = VK(access_token)
    vk.get_photo(vk_id)
    ya = YaUploader(ya_token)
    for path_to_file in os.listdir('photos'):
        ya.upload(file_path=path_to_file, filename=path_to_file)
    upload_google()
    bar.finish()

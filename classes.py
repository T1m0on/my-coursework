import requests
import json
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime
from progress.bar import IncrementalBar
import time
import os

bar = IncrementalBar('Countdown', max = 35)

def get_progress():
        bar.next()
        time.sleep(0.03)

class VK:

    def __init__(self, access_token, version='5.131'):
        self.token = access_token
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.url = 'https://api.vk.com/method/'

    def get_photo(self, vk_id, album_id='profile'): #album_id = wall
        url = self.url + 'photos.get'
        photo_params = {'owner_id': vk_id, 'extended': 1, 'photo_sizes': 1, 'album_id': album_id}
        response = requests.get(url, params={**self.params, **photo_params})
        get_progress()
        if not os.path.isdir("photos"):
            os.mkdir("photos")
        res = response.json()
        counter = 0
        while counter <= res['response']['count'] or counter <= 5:
            for photo in res['response']['items']:
                get_progress()
                for size in photo['sizes']:
                    if 'w' in size['type']:
                        get_progress()
                        name_file = f'{photo["likes"]["count"]}'
                        counter += 1
                        if os.path.isfile(f'{os.path.join(os.getcwd(), "photos", name_file)}.jpeg') is False:
                            photo_info = {'file_name': str(photo["likes"]["count"]), 'size': 'w'}
                            get_progress()
                            with open(f'{os.path.join(os.getcwd(), "photos", name_file)}.jpeg', "wb") as p:
                                resp = requests.get(size['url'])
                                p.write(resp.content)
                                get_progress()
                            with open(f'{os.path.join(os.getcwd(), "photos", name_file)}.json', "w") as f:
                                json.dump(photo_info, f, ensure_ascii=False, indent=2)
                                get_progress()
                                print('Фото выгрузилось, совпадений нет')

                        else:
                            date = datetime.utcfromtimestamp(photo['date']).strftime('%Y-%m-%d')
                            name = f'{str(photo["likes"]["count"])} {date}'
                            photo_info = {'file_name': name, 'size': 'w'}
                            get_progress()
                            with open(f'{os.path.join(os.getcwd(), "photos",name)}.jpeg', "wb") as p:
                                resp = requests.get(size['url'])
                                p.write(resp.content)
                                get_progress()
                            with open (f'{os.path.join(os.getcwd(), "photos",name)}.json', "w") as f:
                                json.dump(photo_info, f, ensure_ascii=False, indent=2)
                                print('Фото выгрузилось, есть совпадения')
                                get_progress()
            return response.json()

class YaUploader:

    def __init__(self, token: str):
        self.token = token
        self.url = 'https://cloud-api.yandex.net/v1/disk/resources/'

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def create_new_folder(self, new_folder):
        folder_url = self.url
        headers = self.get_headers()
        params = {'path': new_folder}
        requests.put(folder_url, headers=headers, params=params)
        print('Папка создана')
        return new_folder

    def get_upload_link(self, disk_fil_path):
        folder = self.create_new_folder('netology')
        upload_url = self.url + 'upload'
        headers = self.get_headers()
        params = {'path':  f"{folder}/{disk_fil_path}", 'overwrite': 'true'}
        response = requests.get(upload_url, headers=headers, params=params)
        get_progress()
        print('Ссылка получена')
        return response.json()

    def upload(self, file_path: str, filename):
        photo = os.path.join(os.getcwd(), 'photos', filename)
        href = self.get_upload_link(disk_fil_path=file_path).get('href', '')
        params = {'overwrite': 'true'}
        response = requests.put(href, params=params, data=open(photo, 'rb'))
        response.raise_for_status()
        get_progress()
        if response.status_code == 201:
            print('Succes')





def upload_google():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    for file_name in os.listdir('photos'):
        photo = drive.CreateFile({'title': file_name})
        photo.Upload()
    print('Done')

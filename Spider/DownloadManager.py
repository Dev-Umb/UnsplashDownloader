from queue import Queue
from threading import Thread
from typing import Dict

import requests

download_queue = Queue()
import uuid


class Downloader:

    def is_over(self):
        return self.over_download

    def __init__(self):
        self.over_download = False
        self.download_manage = Thread(target=self.download)
        self.download_manage.start()

    def set_over(self):
        self.over_download = True

    @staticmethod
    def put_download_url(pic: Dict[str,str]):
        download_queue.put(pic)

    def download(self):
        print("start download listen")
        session = requests.session()
        while not self.over_download or not download_queue.empty():
            if not download_queue.empty():
                print(f"download queue has {download_queue.qsize()} pic")
                pic = download_queue.get()
                tag = pic['tag']
                url = pic['url']
                response = session.get(url)
                name = url.split('/')[-2]
                pic_uuid = f'{tag}/{name}.png'
                with open(f'./File/{pic_uuid}', 'wb') as f:
                    f.write(response.content)
                    f.close()
                print(f'success download {pic_uuid}.png')
        print("over download")

    def join(self):
        self.download_manage.join()

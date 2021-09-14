from Spider import *
from config import *
import os

if __name__ == '__main__':
    session = requests.session()
    downloads = []
    for i in range(0, 4):
        downloads.append(Downloader())
    if not os.path.exists(f'./File'):
        os.mkdir(f'./File')
    for tag in tags:
        if not os.path.exists(f'./File/{tag}'):
            os.mkdir(f'./File/{tag}')
        search_url = f'{url}{keyword}?query={tag}'
        with open('download_url.txt', 'a+') as f:
            first_page = session.get(search_url, headers=headers).json()
            all_page_num = int(first_page['total_pages'])
            if all_page_num > download_pages:
                all_page_num = download_pages
            for page in range(1, all_page_num):
                dataset = session.get(search_url + f'&page={page}', headers=headers).json()['results']
                for data in dataset:
                    download_url = data['links']['download']
                    f.write(download_url + '\n')
                    Downloader.put_download_url(pic={
                        'tag': tag,
                        'url': download_url
                    })
            f.close()
    for i in range(0, 4):
        downloads[i].set_over()
        downloads[i].join()

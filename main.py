import time
from json import JSONDecodeError

from Spider import *
from config import *
import os


def get_first_page(search_url: str):
    token_num = 0
    response = session.get(search_url, headers=headers)
    while response.status_code != 200:
        token_num += 1
        if token_num == len(access_token):
            print("waitting...download")
            time.sleep(1000 * 60)
            token_num = 0
        headers.get('Authorization').format(access_token[token_num])
        response = session.get(search_url, headers=headers)
    page = response.json()
    return page


def push_download_url(search_url, first_page):
    with open('download_url.txt', 'a+') as f:
        all_page_num = int(first_page['total_pages'])
        if all_page_num > download_pages:
            all_page_num = download_pages
        for page in range(1, all_page_num):
            response = session.get(search_url + f'&page={page}', headers=headers)
            while response.status_code == 403:
                print("waitting...download")
                time.sleep(1000 * 60)
                response = session.get(search_url + f'&page={page}', headers=headers)
            dataset = response.json()['results']
            for data in dataset:
                download_url = data['links']['download']
                f.write(download_url + '\n')
                Downloader.put_download_url(pic={
                    'tag': tag,
                    'url': download_url
                })
        f.close()


if __name__ == '__main__':
    headers = {
        'Authorization': f'Client-ID {access_token[0]}'
    }  # 请求头（不需要改）
    session = requests.session()
    downloads = []
    for i in range(0, 4):
        downloads.append(Downloader())
    if not os.path.exists(f'./File'):
        os.mkdir(f'./File')
    # try:
    for tag in tags:
        if not os.path.exists(f'./File/{tag}'):
            os.mkdir(f'./File/{tag}')
        search_url = f'{url}{keyword}?query={tag}'
        first_page = get_first_page(search_url)
        push_download_url(search_url=search_url, first_page=first_page)
    # except Exception as e:
    #     print(e)
    #     pass
    for i in range(0, 4):
        print(f"get pic over.....{i}")
        downloads[i].set_over()
        downloads[i].join()

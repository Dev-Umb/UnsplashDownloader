access_token = ''  # 你的accessKey
url = f'https://api.unsplash.com'
keyword = '/search/photos/'
headers = {
    'Authorization': f'Client-ID {access_token}'
}  # 请求头（不需要改）
tags = ['girl', 'boy']  # 爬取的tag，可以自行按照实例格式编辑增加
download_pages = 10  # 下载最大页数,不要太大,不然可能时间过长

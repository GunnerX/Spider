import os
import time
from concurrent import futures

import requests
from bs4 import BeautifulSoup

# 设置最大重新连接次数
requests.adapters.DEFAULT_RETRIES = 5

# 域名
top_url = 'https://www.ho5ho.com'
# 请求url列表
urls = ['{}/page/{}'.format(top_url, i) for i in range(1,33)]
# 请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
}


# 请求一个url
def req_url(url):
    try:
        r = requests.get(url=url, headers=headers)
        r.keep_alive = False
        r.raise_for_status()
    except:
        print('失败! {}'.format(url))
    else:
        return r

# 取得一个页面内的所有漫画名并写入文件保存
def get_name(url):
    html = BeautifulSoup(req_url(url).text, 'lxml')
    for h5 in html.find_all('h5')[1:]:
        name = h5.a.get_text()
        print(name)
        with open('names.txt', 'a') as f:
            f.write(name)
            f.write('\n')

if __name__ == '__main__':
    with futures.ThreadPoolExecutor(max_workers=8) as pool:
        tasks = [pool.submit(get_name, url) for url in urls]





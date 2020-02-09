import os
import time
from concurrent import futures

import requests
from bs4 import BeautifulSoup

from send_email import send

# 设置最大连接数
requests.adapters.DEFAULT_RETRIES = 5

# 打开爬好的漫画名字文件并构建列表names
with open('names.txt','r') as f:
    names = [line.rstrip('\n') for line in f]

# 域名，请求头
url = 'https://www.xxxxx.com'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
}


def req_url(url):
    attempts = 0
    success = False
    while attempts < 10 and not success:
        try:
            r = requests.get(url=url, headers=headers)
            r.keep_alive = False
            success = True
        except:
            time.sleep(2)
            attempts += 1
            if attempts == 10:
                print('失败! {}'.format(url))
                break
    return r

# 取得当前漫画总页数
def get_page(name):
    name_url = '{}/中字h漫/{}/1'.format(url, name)
    html = BeautifulSoup(req_url(name_url).text, 'lxml')    # 解析html页面以找到页数
    select = html.find('select', id='single-pager')
    pages = (len(select.contents) - 1) // 2
    return pages

# 请求图片真实url并保存在本地
def get_jpg(name):
    stime = time.time()
    os.mkdir('jpgs/{}'.format(name))
    pages = get_page(name)      # 取得当前漫画总页数
    print('{} 总页数: {}'.format(name, pages))
    for page in range(1,pages+1):       # 遍历全部页码
        page_url = '{}/中字h漫/{}/1/p/{}'.format(url, name, page)
        html = BeautifulSoup(req_url(page_url).text, 'lxml')
        img = html.find('img',id='image-{}'.format(page-1))     # 取得图片所在标签
        jpg_url = img.attrs['data-src']         # 取得图片真实地址
        jpg = req_url(jpg_url).content          # 下载图片
        with open('jpgs/{}/{}.jpg'.format(name,page), "wb")as f:   # 存入本地
            f.write(jpg)
        print('{} {}.jpg 保存完成!'.format(name,page))
    etime = time.time()
    print('**** ****')
    print('{}  全部保存完成，耗时 {:.2f}s'.format(name, etime-stime))
    print('**** ****')
    return name

if __name__ == '__main__':
    start_time = time.time()

    os.mkdir('jpgs')
    with futures.ThreadPoolExecutor(max_workers=15) as pool:    # 线程池，最大30个线程
        tasks = [pool.submit(get_jpg, name) for name in names]
        for task in futures.as_completed(tasks):
            print('----线程结束!----')

    time_sec = time.time() - start_time
    time_min = time_sec / 60
    time_hou = time_min / 60
    print('全部完成, 耗时 {:.2f}s! 即{:.2f}分钟,即{:.2f}小时'.format(time_sec, time_min, time_hou))
    send()









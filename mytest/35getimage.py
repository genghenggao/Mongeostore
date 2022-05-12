'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2021-05-12 09:44:35
LastEditors: henggao
LastEditTime: 2021-05-12 09:44:52
'''
'''
@Description: 
@Version: 1.0
@Autor: Henggao
@Date: 2020-02-21 12:32:03
@LastEditors: Henggao
@LastEditTime: 2020-02-21 12:32:17
'''
"""
用os模块，requests,re来爬取妹子图片
url网址：http://www.zdqx.com/qingchun/
"""
import requests
import re,os,time

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
    'referer': 'http://www.zdqx.com/pcbz/70270.html',
    'cookie': 'Hm_lvt_303a32038183efa6d8efec90c0031b87=1581472898; Hm_lpvt_303a32038183efa6d8efec90c0031b87=1581472912'
}

def get_urls(url):
    response = requests.get(url=url, headers=headers)
    response.encoding = response.apparent_encoding
    result1 = re.findall('<div class="listbox">(.*?)</div>', response.text, re.S)
    result2 = re.findall('<img src="(.*?)" alt="(.*?)">', str(result1), re.S)
    for url, title in result2:
        url = 'http:' + str(url)
        title = title.replace(r'" height="281', '')
        savedata(url, title)

def savedata(url,title):
    path = '小姐姐图片'
    if not os.path.exists(path):
        os.mkdir(path)
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    with open(path + '/' + title + '.jpg',mode="wb") as f:
        f.write(response.content)
    print(title+'保存成功！')
    f.close()

if __name__ == '__main__':
    for page in range(2,4):
        if page == 1:
            url = 'http://www.zdqx.com/qingchun/index.html'
        else:
            url ='http://www.zdqx.com/qingchun/index_' + str(page) + '.html'
        get_urls(url)
        print('第'+str(page-1)+'采集完毕！')
        time.sleep(2)
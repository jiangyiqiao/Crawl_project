#coding=utf-8
from threading import Thread
import requests
import re
import os


def get_page_url(url, param):
    response = requests.get(url, params=param)
    response.encoding = 'utf-8'
    return response.text


def parse_page(str):
    pattern = re.compile('"middleURL":"(.*?)",') #use regu match picture url
    url_list = re.findall(pattern, str)
    return url_list

'''
#单线程下载
def run(keyword, path):
    url = "https://image.baidu.com/search/acjson"
    i = 0
    for j in range(30, 100, 30):
        params = {"ipn": "rj", "tn": "resultjson_com", "word": keyword, "pn": str(j)}
        html = get_page_url(url, params)
        lists = parse_page(html)
        for item in lists:
            try:
                img_data = requests.get(item, timeout=10).content
                with open(path + "/" + str(i) + ".jpg", "wb") as f:
                    f.write(img_data)
                    print("process run save images to ",img_data)
                    f.close()
                i = i+1
            except requests.exceptions.ConnectionError:
                print('can not download')
                continue
'''
def download(url,path,picture_seq):
    try:
        img_data = requests.get(url, timeout=10).content
        with open(path + "/" + str(picture_seq) + ".jpg", "wb") as f:
            f.write(img_data)
            print("process run save images to ",path)
            f.close()
    except requests.exceptions.ConnectionError:
        print('can not download')
        return

def run(keyword, path):
    url = "https://image.baidu.com/search/acjson"
    picture_seq=0
    lists=[]
    for j in range(30, 220, 30):
        params = {"ipn": "rj", "tn": "resultjson_com", "word": keyword, "pn": str(j)}
        html = get_page_url(url, params)
        html_lists = parse_page(html)
        for html_list in html_lists:
            lists.append(html_list)

    for i in range(0,len(lists),40):
        print(i)
        if i+40 > len(lists):return
        tasks = lists[i:i+40]
        threads = []
        print("progress "+str(i)+'/'+str((len(lists))))
        for url in tasks:
            t = Thread(target=download, args=(url, path,picture_seq))
            picture_seq=picture_seq+1
            threads.append(t)
            t.start()
        for t in threads:
            t.join()


def make_dir(keyword):
    path = "pictures/"+str(keyword)
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path)
        return path
    else:
        print(path + 'path has already exits')
        return path




if __name__ == '__main__':
    keywords = ["中年人"]
    for keyword in keywords:
        path = make_dir(keyword)
        run(keyword, path)
        print("finished keyword ",keyword)

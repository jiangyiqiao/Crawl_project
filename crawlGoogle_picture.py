#coding=utf-8
from threading import Thread
import requests
import urllib
import json
import os
'''
proxies={
    'http':'socks5://127.0.0.1:1080',
    'https':'socks5://127.0.0.1:1080'
}
'''
d = {
        '李鹏':'lipeng',
        '蔡奇':'caiqi',
        '郭声琨':'guoshengkun',
        '李鸿忠':'lihongzhong',
        '应勇':'yingyong',
        '曾庆红':'zengqinghong',
        '邓小平':'dengxiaoping',
        '胡锦涛':'hujintao',
    '江泽民':'jiangzemin','毛泽东':'maozedong','温家宝':'wenjiabao','赵紫阳':'zhaoziyang','朱镕基':'zhurongji',
    '薄熙来':'boxilai','郭伯雄':'guoboxiong','令计划':'linjihua','徐才厚':'xucaihou','周永康':'zhouyongkang'
}

headers = {
           'authority':'www.google.com',
           'method':'GET',
           'cookie':'S_adsense3-ui=iJNUZE1Yy_oNmwqsZk_qmkXPuR7VOdcK; OTZ=4164008_24_24__24_; SID=eQX2SMR3Y5ARnEUQtDAK9fOp-JCa0G6v1sxzKoeYb6ZYYOGKs8Fa1qGsy836hkmyvGxfbA.; HSID=AaQqqA5h2fyfMy8Fb; SSID=Awr_x4f-SsFpAc6H8; APISID=-vGBPOriYoS3SvvC/AhHD5I5rj3cz2SEPY; SAPISID=l2xHrtcyFnPWv96S/AstaVXf6d-TkPgKLn; S=adsense3-ui=LnDygd2-7ogZM-Q6yKfH72-fDvYsrCNK:adwords-usermgmt=9ZR0CVdmldoRQfqDPvCRzLWFfKs5vk8I:adwords-kwoptimization=VaeUXlqDX8c9VvQd-bzolOUq8R4Qabpk:adwords-common-ui=Mwi6wiJLbcgI6zQpRFSM6Dlk_-AbrD5h:adwords-navi=C_9FlnP6FOJL8z3JBam_F0ieuZ56D_Bt; NID=119=DHM-TtK5X4yYysWqN-_VtH9uw6etdyu_8lVcdu8sHLEQUJjGaCaVDjn1YjkZnnyRUcFhsdAch92HgQSEP4OX_8xrYey96nltKm0qaWb261TdKg2xXFxMUiXZ7hX7iMC4C49DXhIEcPC4Iu-alt4RDTGRM135rC0Jj7v-FwBrJ_XWgNsEWAG8S8QNHkWExLDbA5K7Vv2VzuySVo0PnypNHgbJ4Q6QMS1XPnlFlQK3l93QzuZtsDhgt4I4jWml; DV=U9ZPFEVJIQpKIJNxYlFnT2mDxF-NBVZqsIJhmEcShwsAAJDY_A7G1-0XPoEAABxSTvlwqJOieiAAAA; 1P_JAR=2017-12-15-6; SIDCC=AE4kn78anNPHP_9_xGLKQwHroW_OXi7x6OxebcC361Oca6lI7V0KJTpTwB15yYE0pmsbnImIYaau-ULanFkukA',
            'referer':'https://www.google.com/',
 'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36',
}

#获取到每一百页图片的url
def getURL(name):
    web_url = []
    key_word={'q':name}
    url_start="https://www.google.com.hk/search?ei=57YwWvr0Oovo0gSW4JuYBg&safe=strict&yv=2&tbm=isch&"

    key=urllib.urlencode(key_word)
    #print(key)
    url_mid="&vet=10ahUKEwi6hLSXnYbYAhULtJQKHRbwBmMQuT0IOigB.57YwWvr0Oovo0gSW4JuYBg.i&ved=0ahUKEwi6hLSXnYbYAhULtJQKHRbwBmMQuT0IOigB&i"
    url_end="&asearch=ichunk&async=_id:rg_s,_pms:s"
    for i in range(1,2):
        web_url.append(url_start+key+url_mid+"jn="+str(i)+"&"+"start="+str(i*100)+url_end)
    #print(web_url)
    return web_url

#获取web_url的数据，转为json，并用data列表存储
def to_json(web_url):
    datas=[]
    for url in web_url:
        try:
            web_jsondata=requests.get(url,headers=headers)
            print(web_jsondata.text)
            datas.append(web_jsondata.text)
        except:
            continue
   #print(data)
    return datas

#对每个列表的数据分割出图片url放入picture——url
def parse(datas):
    picture_url = []

    for data in datas:
        results = data.split("rg_meta notranslate")
        if len(results)>1:
            results = results[1:]
        else:
            return picture_url

        for result in results:

            result = result[8:result.find('}')+1]
            result = result.replace('\\','')
            print(result)
            d = {}
            try:
                d = json.loads(result)
            except Exception,e:
                print("json loads exception "+str(e))
                continue
            if "ou" in d:
                picture_url.append(d["ou"])
                print(d["ou"])
    return picture_url


def download(url, filepath):
    try:
        print("processing url is " +url)
        response = requests.get(url,timeout=10)
        picture = open(filepath, "wb")
        picture.write(response.content)
        print("processing url end "+url+ " filepath is "+filepath)
    except Exception,e:
        print("error occur on "+str(e))
        if e==requests.exceptions.ConnectTimeout:
            print("begin connectTimeout error redownload progress"+url+""+filepath)
            download(url, filepath)
        elif e==requests.exceptions.Timeout:
            print("begin Timeout error redownload progress" + url + "" + filepath)
            download(url, filepath)
        return


def savePicture(picture_url, directory):
    num=0
    for i in range(0,len(picture_url),20):
        if i+20 > len(picture_url):return
        tasks = picture_url[i:i+20]
        threads = []
        print("progress "+str(i)+'/'+str((len(picture_url))))
        for url in tasks:
            num+=1
            filepath = directory + '/' + url[-30:-5].encode("utf-8").replace("/", "") + "_" + str(num) + ".jpg"
            t = Thread(target=download, args=(url, filepath.decode("utf-8")))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()



if __name__=='__main__':
    policy_name =['蔡奇']
    #policy_name=['郭声琨','李鸿忠','应勇','曾庆红','邓小平','胡锦涛','江泽民','李鹏','毛泽东','温家宝','赵紫阳','朱镕基','毛泽东','薄熙来','郭伯雄','令计划','徐才厚','周永康']
    for name in policy_name:
        name_pinyin = d[name]
        directory = "pictures/" + name_pinyin
        if not os.path.exists(directory):
            os.makedirs(directory)
        web_url = getURL(name)
        print(len(web_url))
        data=to_json(web_url)
        picture_url = parse(data)
        print("url number "+str(len(picture_url)))
        print("begin save picture")
        savePicture(picture_url,directory)
        print("over")


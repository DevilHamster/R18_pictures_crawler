import requests
from lxml import etree
import time
import os
import random
from tqdm import tqdm, trange

switch_url = "跳转页面" #多数此类网站会变更域名，在变更域名后旧域名会作为跳转页面，可长期用来捕获主页
headers = {
    "User-Agent":"xxx" #UA伪装
    }
LabelList = ['xxx','xxx','xxx','xxx'] #板块分类
Filepath_ex = 'path' #文件路径
Section_endings = [
    '/xxx',
    '/xxx', 
    '/xxx', 
    '/xxx', 
    ] #各板块对应的url后缀
pages = 1 #每个版块爬取1页

#根据跳转页面截获现在的主页网站url,没有这个链接什么也做不了
def GetMainUrl(): 
    try:
        resp = requests.get(url = switch_url, allow_redirects=False)
        current_url = resp.headers['location']
        return current_url
    except:
        print("跳转链接失效,程序将自动退出")
        os._exit()

#通过帖子的url下载一个帖子内的图片
def DownloadSinglePage(url): 
    try:
        resp = requests.get(url=url,headers=headers)
        if(resp.status_code != 200): return
        html = etree.HTML(resp.text)
        label = html.xpath("/xpath语句") #获取帖子所属板块
        title = html.xpath("/xpath语句") #获取帖子标题
        #print(title)
        #下载下来的文件存放在如下路径：Filepath_ex + label + "/" + title
        if os.path.exists(Filepath_ex + label + "/" + title):
            return
        else:
            time.sleep(random.uniform(1.0,2.0)) #防封禁
            os.makedirs(Filepath_ex + label + "/" + title) #创建路径
            img_list = html.xpath("/xpath语句") #获取所有图片的链接
            #逐个下载图片，并用进度条记录
            for i in tqdm(iterable = range(0, len(img_list)), desc = title, unit='pic'):
                time.sleep(random.uniform(1.2,2.0)) #防封禁
                download(img_list[i], Filepath_ex + label + "/" + title + "/" + str(i+1) + '.jpg')
            print(title + "抓取成功...")
    except:
        print("Error: something weird just happened, this post will be lost.")
        
#通过链接下载单张图片，下不到就算了
def download(img_url, filepath):
    try:
        r = requests.get(url = img_url, headers=headers)
        with open(filepath,'wb') as f:
            f.write(r.content)
    except:
        print("Error: something weird just happened, few images will be lost.")

#获取某个版块下pages页内所有帖子url
def PostsCollect(cur_url, url_ending, pages): 
    url_list = []
    for i in range(0,pages):
        result = requests.get(url = cur_url + url_ending + str(i+1) + '.html', headers=headers)
        html = etree.HTML(result.text)
        url_list.extend(html.xpath("/xpath语句"))
        time.sleep(random.uniform(2.3,3.5)) #随机暂停
    return url_list

if __name__ == '__main__':
    current_url = GetMainUrl() #获取主页url
    posts = [] #这个列表存放收集到的所有帖子的url
    for ending in tqdm(iterable = Section_endings, desc = '各版块图片帖链接获取中', unit='section'):
        posts.extend(PostsCollect(current_url, ending, pages=pages))
    print("图片帖链接抓取成功! 接下来进行下载...")
    time.sleep(2) #防封禁
    for post in posts:
        DownloadSinglePage(url=current_url + '/' + post)
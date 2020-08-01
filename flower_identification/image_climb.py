#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import re, requests, os
from urllib import error

# 想要下载图片的数量
numPicture = 0
# 显示下载第几张图片
num = 0
# 下载至该路径文件夹
file = ''
# 辅助统计图片总数
List = []


# 获取查找的关键词信息获取图片url地址
def getURL(url):
    global List
    print('正在检测图片总数.....')
    t = 0
    s = 0
    while t < 1000:
        Url = url + str(t)
        try:
            Result = requests.get(Url)
        except BaseException:
            t = t + 60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result)
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s


# 下载图片
def dowmloadPicture(html, keyword):
    global num
    pic_url = re.findall('"objURL":"(.*?)",', html)
    print('找到关键词:' + keyword + '的图片，即将下载图片...')
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载')
            continue
        else:
            string = file + r'\\' + keyword + '_' + str(num) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close()
            num += 1
        if num >= numPicture:
            return


if __name__ == '__main__':
    word = input("请输入搜索关键词>>>")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=' + word + '&pn='
    t = getURL(url)
    print('%s类图片共有%d张' % (word, t))
    numPicture = int(input('请输入想要下载的图片数量>>>'))
    file = input('请输入存储图片的文件夹名称>>>')

    y = os.path.exists(file)
    if y == 0:
        print('该文件不存在，请重新输入>>>')
        file = input('请输入存放图片的文件夹名称>>>')

    t = 0
    tmp = url
    while t < numPicture:
        try:
            url = tmp + str(t)
            result = requests.get(url)
            print(url)
        except error.HTTPError as err:
            print('网络错误，请调整网络后重试')
            t = t + 60
        else:
            dowmloadPicture(result.text, word)
            t = t + 60
    print('结束')

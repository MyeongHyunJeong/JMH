# -*- coding: utf-8 -*-
import datetime
import json
import urllib.request
import csv
import matplotlib.pyplot as plt
import numpy as np

from bs4 import BeautifulSoup

dataCnt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def getInfo(_url):
    sourcecode = urllib.request.urlopen(_url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    if _url == "https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&pkid=110&os=2262029&query=%EC%96%91%ED%8F%89%20%EB%8C%80%EC%9E%90%EC%97%B0%20%EB%B9%99%EC%96%B4%EC%86%A1%EC%96%B4%EC%B6%95%EC%A0%9C":
        return {}

    img_url = soup.select("div.thumb_box a img")[0]['src']
    title = soup.select("div.info_box h4 a")[0]['alt']
    sub_title = soup.select("div.ftv_info p")[0].text


    sub_info_title = []
    sub_info_text = []
    info_result = {}
    info_result['img_url'] = img_url
    for i in soup.select("dl.ftv_oth_info")[0].find_all('dt'):
        sub_info_title.append(i.get_text())
    for i in soup.select("dl.ftv_oth_info")[0].find_all('dd'):
        if str(i).find('href') != -1:
            sub_info_text.append(i.find('a')['href'])
        else:
            sub_info_text.append(i.get_text())

    for i in range(0, len(sub_info_title)):
        info_result[sub_info_title[i]] = sub_info_text[i]

    return info_result

# URL정하는 함수
def getSeasonUrl(text):
    month = datetime.date.today().month

    # URL 데이터를 가져올 사이트 url 입력
    url_spring = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&query=%EB%B4%84%EC%B6%95%EC%A0%9C'
    url_summer = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&query=%EC%97%AC%EB%A6%84%EC%B6%95%EC%A0%9C'
    url_fall = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&query=%EA%B0%80%EC%9D%84%EC%B6%95%EC%A0%9C'
    url_winter = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=bk00&query=%EA%B2%A8%EC%9A%B8%EC%B6%95%EC%A0%9C'

    if text == '축제':
        if month == 1 or month == 2 or month == 12:
            url = url_winter
        elif month == 3 or month == 4 or month == 5:
            url = url_spring
        elif month == 6 or month == 7 or month == 8:
            url = url_summer
        elif month == 9 or month == 10 or month == 11:
            url = url_fall

    elif text == '봄':
        url = url_spring
    elif text == '여름':
        url = url_summer
    elif text == '가을':
        url = url_fall
    elif text == '겨울':
        url = url_winter
    else:
        url = 'Error'

    return url


# 크롤링 함수 구현하기
def execute(text):
    # 여기에 함수를 구현해봅시다.

    # text에 따른 URL
    # 봄, 여름, 가을, 겨울의 뒷 URL
    spring = '%EB%B4%84%EC%B6%95%EC%A0%9C'
    summer = '%EC%97%AC%EB%A6%84%EC%B6%95%EC%A0%9C'
    fall = '%EA%B0%80%EC%9D%84%EC%B6%95%EC%A0%9C'
    winter = '%EA%B2%A8%EC%9A%B8%EC%B6%95%EC%A0%9C'

    # URL 데이터를 가져올 사이트 url 입력
    url = getSeasonUrl(text)

    d_info_list = []

    # soup 설정
    req = urllib.request.Request(url)
    sourcecode = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(sourcecode, "html.parser")

    Festival_Detail_Info(text, soup)

    # text에 따라 축제정보 저장하기
    if spring in url:
        festival_info = Festival_Infomation(text, soup, url)
    elif summer in url:
        festival_info = Festival_Infomation(text, soup, url)
    elif fall in url:
        festival_info = Festival_Infomation(text, soup, url)
    elif winter in url:
        festival_info = Festival_Infomation(text, soup, url)
    else:
        print("Fail")
        # if text in festival_detail_info.keys():
        #     print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHI")
        # else:
        #     print("wrong text")

    # tDict = getInfo(festival_detail_info[text])
    #
    # d_info_list.append(tDict['img_url'])
    # for i, j in tDict.items():
    #     if i == 'img_url':
    #         continue
    #     d_info_list.append("\n" + i + " : " + j)


def Festival_Detail_Info(text, soup):
    url_temp = []
    list_url = []
    ftv_tit = []
    festival_detail_info = {}

    # 원하는 축제 URL 저장
    for i in str(soup.find_all("div", class_="ftv_lst")).split('<a'):
        if str(i).find('href=\"') == 1:
            url_temp.append("https://search.naver.com/search.naver" + str(i)[7:str(i).find('\" nocr')])

    for i in url_temp:
        str1 = ""
        for j in i.split("amp;"):
            str1 = str1 + j
        list_url.append(str1)

    for tit in soup.find_all("h5"):
        ftv_tit.append(tit.get_text().strip())

    for i in range(len(ftv_tit)):
        festival_detail_info[ftv_tit[i]] = list_url[i]

    filename = ''
    if text == '봄':
        filename = 'spring_detailed.csv'
    elif text == '여름':
        filename = 'summer_detailed.csv'
    elif text == '가을':
        filename = 'fall_detailed.csv'
    else:
        filename = 'winter_detailed.csv'
    f = open(filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)

    for key in festival_detail_info:
        wr.writerow(getInfo(festival_detail_info[key]).values())

    f.close()

# 축제 정보정리하기
def Festival_Infomation(text, soup, url):
    # 축제정보(축제이름, 장소, 날짜) 리스트 생성
    festival_info_bs = []
    ftv_tit = []
    ftv_loc = []
    ftv_date = []

    for tit in soup.find_all("h5"):
        ftv_tit.append(tit.get_text().strip())

    for loc in soup.find_all("span", class_="local_box"):
        ftv_loc.append(loc.get_text().strip())

    for date in soup.find_all("span", class_="date"):
        ftv_date.append(date.get_text().strip())

    filename = ''
    if text == '봄':
        filename = 'spring.csv'
    elif text == '여름':
        filename = 'summer.csv'
    elif text == '가을':
        filename = 'fall.csv'
    else:
        filename = 'winter.csv'

    f = open(filename, 'w', encoding='utf-8', newline='')
    wr = csv.writer(f)

    for i in range(len(ftv_tit)):
        if int(str(ftv_date[i][5])) == 0:
            dataCnt[int(str(ftv_date[i])[6:7]) - 1] = dataCnt[int(str(ftv_date[i])[6:7]) - 1] + 1
        else:
            dataCnt[int(str(ftv_date[i])[5:7]) - 1] = dataCnt[int(str(ftv_date[i])[5:7]) - 1] + 1

        wr.writerow([ftv_tit[i], ftv_loc[i], ftv_date[i]])

    f.close()

    return festival_info_bs

if __name__ == '__main__':
    print('수집시작')

    execute("봄")
    execute("여름")
    execute("가을")
    execute("겨울")

    labels = ['spring', 'summer', 'fall', 'winter']
    springCnt = dataCnt[0] + dataCnt[1] + dataCnt[11]
    summerCnt = dataCnt[2] + dataCnt[3] + dataCnt[4]
    fallCnt = dataCnt[5] + dataCnt[6] + dataCnt[7]
    winterCnt = dataCnt[8] + dataCnt[9] + dataCnt[10]

    colors = ['gold', 'lightskyblue', 'orange', 'olive']
    patches, texts = plt.pie([springCnt, summerCnt, fallCnt, winterCnt],
                             colors=colors, shadow=True, startangle=90)
    plt.legend(patches, labels, loc="best")
    plt.axis('equal')
    plt.tight_layout()
    plt.savefig('season_cnt.png')
    #
    # objects = ('Spring', 'Summer', 'Fall', 'Winter')
    # y_pos = np.arange(len(objects))
    #
    # plt.bar(y_pos, [springCnt, summerCnt, fallCnt, winterCnt], color=colors, align='center')
    # plt.xticks(y_pos, objects)
    # plt.ylabel('Count')
    #
    # plt.savefig('cnt.png')

    print("수집 끝")
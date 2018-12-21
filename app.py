# -*- coding: utf-8 -*-
import datetime
import json
import os
import re
import csv
import urllib.request

from bs4 import BeautifulSoup
from slackclient import SlackClient
from flask import Flask, request, make_response, send_file, render_template
import csv

app = Flask(__name__)

slack_token = 'xoxb-504131970294-507702271989-5zBFhbconrtl6ePTzgriXNqB'
slack_client_id = '504131970294.506896729057'
slack_client_secret = '2817eff0bae4f99c570f6d8c3d0fd4ed'
slack_verification = 'rGC5JnRYaHdFArfqeHXyhbrr'
sc = SlackClient(slack_token)

spring_data = []
summer_data = []
fall_data = []
winter_data = []
total_data = []

spring_detailed_data = []
summer_detailed_data = []
fall_detailed_data = []
winter_detailed_data = []
total_detailed_data = []

gumi_data = []
daegu_data = []
busan_data = []
pohang_data = []

def print_book_info():

    loc_list = ['대구', '부산', '포항', '구미']
    tit = []
    local = []
    location = []
    date = []
    info = []
    corp = []
    tel = []
    url = []

    for loc in loc_list:
        if loc == '대구':
            filename = 'daegu.csv'
        elif loc == '부산':
            filename = 'busan.csv'
        elif loc == '포항':
            filename = 'pohang.csv'
        elif loc == '구미':
            filename = 'gumi.csv'

        with open(filename) as file:
            # ',' 기호로 분리된 CSV 파일을 처리하세요..
            reader = csv.reader(file, delimiter=',')

            # 처리된 파일의 각 줄을 불러옵니다.
            for row in reader:
                ftv_tit = row[0]
                ftv_loc = row[1]
                ftv_date = str(row[2]).replace("-", ".") + "~" + str(row[3]).replace("-", ".")
                ftv_info = row[4]
                ftv_corp = row[5]
                ftv_tel = row[8]
                ftv_url = row[9]

                if loc == '대구':
                    daegu_data.append([ftv_tit, ftv_loc, ftv_date])
                if loc == '부산':
                    busan_data.append([ftv_tit, ftv_loc, ftv_date])
                if loc == '포항':
                    pohang_data.append([ftv_tit, ftv_loc, ftv_date])
                if loc == '구미':
                    gumi_data.append([ftv_tit, ftv_loc, ftv_date])

                print("{} / {} / {}".format(ftv_tit, ftv_loc, ftv_date))
                local.append(loc)
                tit.append(ftv_tit)
                location.append(ftv_loc)
                date.append(ftv_date)
                info.append(ftv_info)
                corp.append(ftv_corp)
                tel.append(ftv_tel)
                url.append(ftv_url)

    dst_file = 'local.csv'
    f = open(dst_file, 'w', newline='')
    csv.writer = csv.writer(f)
    for i in range(len(local)):
        csv.writer.writerow([local[i], tit[i], location[i], date[i], info[i], corp[i], tel[i], url[i]])
    f.close()

def loadSpring():
    f = open('spring.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        spring_data.append(line)
    f.close()

    f = open('spring_detailed.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)

    tmp = {}
    for line in rdr:
        for idx in range(0, len(line)):
            if idx == 0:
                tmp["URL"] = line[idx]
            elif idx == 1:
                tmp["기간"] = line[idx]
            elif idx == 2:
                tmp["장소"] = line[idx]
            elif idx == 3:
                tmp["주최"] = line[idx]
            elif idx == 4:
                tmp["정보"] = line[idx]
            elif idx == 5:
                tmp["요금"] = line[idx]
        spring_detailed_data.append(tmp)
    f.close()

    return ""

def loadSummer():
    f = open('summer.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        summer_data.append(line)
    f.close()

    f = open('summer_detailed.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)

    tmp = {}
    for line in rdr:
        for idx in range(0, len(line)):
            if idx == 0:
                tmp["URL"] = line[idx]
            elif idx == 1:
                tmp["기간"] = line[idx]
            elif idx == 2:
                tmp["장소"] = line[idx]
            elif idx == 3:
                tmp["주최"] = line[idx]
            elif idx == 4:
                tmp["정보"] = line[idx]
            elif idx == 5:
                tmp["요금"] = line[idx]
        summer_detailed_data.append(tmp)
    f.close()

    return ""

def loadFall():
    f = open('fall.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        fall_data.append(line)
    f.close()

    f = open('fall_detailed.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)

    tmp = {}
    for line in rdr:
        for idx in range(0, len(line)):
            if idx == 0:
                tmp["URL"] = line[idx]
            elif idx == 1:
                tmp["기간"] = line[idx]
            elif idx == 2:
                tmp["장소"] = line[idx]
            elif idx == 3:
                tmp["주최"] = line[idx]
            elif idx == 4:
                tmp["정보"] = line[idx]
            elif idx == 5:
                tmp["요금"] = line[idx]
        fall_detailed_data.append(tmp)
    f.close()

    return ""

def loadWinter():
    f = open('winter.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)
    for line in rdr:
        winter_data.append(line)
    f.close()

    f = open('winter_detailed.csv', 'r', encoding='utf-8')
    rdr = csv.reader(f)

    tmp = {}
    for line in rdr:
        for idx in range(0, len(line)):
            if idx == 0:
                tmp["URL"] = line[idx]
            elif idx == 1:
                tmp["기간"] = line[idx]
            elif idx == 2:
                tmp["장소"] = line[idx]
            elif idx == 3:
                tmp["주최"] = line[idx]
            elif idx == 4:
                tmp["정보"] = line[idx]
            elif idx == 5:
                tmp["요금"] = line[idx]
        winter_detailed_data.append(tmp)
    f.close()

    return ""


def makeTotalData():
    for item in spring_data:
        total_data.append(item)
    for item in summer_data:
        total_data.append(item)
    for item in fall_data:
        total_data.append(item)
    for item in winter_data:
        total_data.append(item)
    print(total_data)

def makeTotalDetailedData():
    for item in spring_detailed_data:
        total_detailed_data.append(item)
    for item in summer_detailed_data:
        total_detailed_data.append(item)
    for item in fall_detailed_data:
        total_detailed_data.append(item)
    for item in winter_detailed_data:
        total_detailed_data.append(item)
    print(total_detailed_data)

def getAnswer(text):
    startLen = text.find('>')
    text = text[startLen + 2:]

    if text == '봄':
        str = u""
        for item in spring_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str
    elif text == '여름':
        str = u""
        for item in summer_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str
    elif text == '가을':
        str = u""
        for item in fall_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str
    elif text == '겨울':
        str = u""
        for item in winter_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str
    elif text == '구미':
        str = u""
        for item in gumi_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str
    elif text == '대구':
        str = u""
        for item in daegu_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str
    elif text == '부산':
        str = u""
        for item in busan_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str
    elif text == '포항':
        str = u""
        for item in pohang_data:
            str = str + item[0] + ' / ' + item[1] + ' / ' + item[2] + '\n'
        return str

    elif text == '계절 통계':
        return 'season'
    elif text == '지역 통계':
        return 'local'
    else:
        for idx in range(0, len(total_data)):
            if text == total_data[idx][0]:
                str = u''
                for key in total_detailed_data[idx]:
                    if key == 'URL':
                        str = total_detailed_data[idx][key] + '\n'
                    else:
                        str = str + key + " : " + total_detailed_data[idx][key] + '\n'
                return str

        return "Re-enter Massage(축제/봄/여름/가을/겨울)"


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        # text='Bugs 실시간 음악 차트 Top 10'

        festival_info = getAnswer(text)
        print(festival_info)

        if festival_info == 'season':
            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text='http://f3764710.ngrok.io/seasoncnt'
            )
        elif festival_info == 'local':
            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text='http://f3764710.ngrok.io/localcnt'
            )
        else:
            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text=festival_info
            )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

@app.route("/localcnt")
def sendLocalCntImg():
    return send_file('local_cnt.png', mimetype='image/png')

@app.route("/seasoncnt")
def sendSeasonCntImg():
    return send_file('season_cnt.png', mimetype='image/png')

@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"

if __name__ == '__main__':
    loadSpring()
    loadSummer()
    loadFall()
    loadWinter()
    makeTotalData()
    makeTotalDetailedData()
    print_book_info()
    app.run('0.0.0.0', port=8080)
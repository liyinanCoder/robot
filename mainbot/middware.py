#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import simplejson
from status import BotStatus


# ai参数
key = '8edce3ce905a4c1dbb965e6b35c3834d'
api_url = 'http://www.tuling123.com/openapi/api'


def tuling_ai(request, group=None):
    submit = {'key': key, 'info': request, 'userid': 'qq-bot'}

    try:
        response = requests.post(api_url, data=submit).text
        result = simplejson.loads(str(response))['text']
        if result is None:
            return ''
        return result
    except Exception:
        return ''


def handle(request, group=None):
    # 处理格式
    # pash|关键词|内容
    tmp = request.split('|')
    db = BotStatus(group)
    if len(tmp) is 3:
        # 命令处理
        if 'push' in tmp[0]:
            db.set_keyword(tmp[1], tmp[2])
            return tmp[2]
        elif 'add' in tmp[0]:
            db.set_all_keyword(tmp[1], tmp[2])
            return tmp[2]
    elif len(tmp) is 2:
        if 'del' in tmp[0]:
            return db.rm_keyword(tmp[1])
        elif 'rm' in tmp[0]:
            return db.rm_all_keyword(tmp[1])
    else:
        return ''


def get_key_value(request, group=None):
    db = BotStatus(group)
    return db.get_keyword(request)


def get_all_key_value(request, group=None):
    db = BotStatus(group)
    return db.get_all_keyword(request)
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import requests
import simplejson
import random
import string
import uuid
from status import BotStatus
import datetime
import time
from urllib.parse import quote
import hashlib
from conf import KEY, APP_ID


# ai参数
api_url = 'https://api.ai.qq.com/fcgi-bin/nlp/nlp_textchat'


def qq_ai(request, group=None):
    submit = {
        'app_id': APP_ID,
        'time_stamp': int(time.mktime(datetime.datetime.now().timetuple())),
        'nonce_str': ''.join(random.sample(
            string.ascii_letters + string.digits, 32)),
        'session': str(uuid.uuid1()).replace('-', ''),
        'question': request,
    }

    # 写入sign
    submit_v = sorted(submit.items(), key=lambda e: e[0], reverse=False)
    sign = ''
    for node in submit_v:
        if sign != '':
            sign = sign + '&'
        sign = sign + '{}={}'.format(node[0], quote(str(node[1])))
    sign = sign + '&app_key={}'.format(KEY)
    hl = hashlib.md5()
    hl.update(sign.encode(encoding='utf-8'))
    submit['sign'] = hl.hexdigest().upper()

    try:
        response = requests.post(api_url, data=submit).text
        result = simplejson.loads(str(response))['data']['answer']
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
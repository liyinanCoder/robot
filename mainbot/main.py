#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from qqbot import QQBotSlot as qqbotslot, RunBot
from middware import tuling_ai, handle, get_key_value
from middware import get_all_key_value


@qqbotslot
def onQQMessage(bot, contact, member, content):
    if bot.isMe(contact, member):
        return
    
    g = str(contact.nick)
    if '@ME' in content:
        bot.SendTo(contact, '@{} '.format(member.name) + getms(content, g))
    else:
        mession = getallms(content, g)
        if mession != '':
            bot.SendTo(contact, mession)


def getms(content, g):
    # 处理请求
    content = content.replace('[@ME]', '').strip()

    # 注册中间件
    mw = [
        handle, get_key_value,
    ]

    result = ''
    for func in mw:
        result = func(content, group=g)
        if not (result is ''):
            break
    if result is '' or result is None:
        result = tuling_ai(content, group=g)
    return result


def getallms(content, g):
    # 处理请求
    content = content.strip()
    # 注册中间件
    mw = [
        get_all_key_value,
    ]

    result = ''
    for func in mw:
        result = func(content, group=g)
        if not (result is ''):
            break
    return result


if __name__ == '__main__':
    RunBot()
#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import redis
from conf import REDIS_ADDR, REDIS_PART


class BotStatus:
    def __init__(self, group):
        self.db = redis.Redis(host=REDIS_ADDR, port=REDIS_PART)
        self.group = str(group)

    def get_status(self, key):
        '''
        -1 为不存在
        '''
        if self.exists():
            return self.db.hget(self.group, key)
        else:
            return -1
    
    def set_status(self, key, value):
        self.db.hset(self.group, key, value)
        return value

    def set_keyword(self, statement, value):
        # TODO 内容检测
        self.db.hset(self.get_kw_db(), statement, value)
        return value

    def get_keyword(self, statement):
        if self.kw_exists():
            # TODO 内容检测
            result = self.db.hget(self.get_kw_db(), statement)
            if result is None:
                return ''
            return str(result, encoding='utf=8')
        else:
            return ''

    def rm_keyword(self, statement):
        # TODO 内容检测
        val = self.db.hdel(self.get_kw_db(), statement)
        if val == 0:
            return '删除失败，可能不存在'
        return '删除[{}]成功'.format(statement)

    # 全局关键词
    def set_all_keyword(self, statement, value):
        # TODO 内容检测
        self.db.hset(self.get_all_kw_db(), statement, value)
        return value

    def rm_all_keyword(self, statement):
        # TODO 内容检测
        val = self.db.hdel(self.get_all_kw_db(), statement)
        if val == 0:
            return '删除失败，可能不存在'
        return '删除[{}]成功'.format(statement)

    def get_all_keyword(self, statement):
        if self.kw_all_exists():
            # TODO 内容检测
            result = self.db.hget(self.get_all_kw_db(), statement)
            if result is None:
                return ''
            return str(result, encoding='utf=8')
        else:
            return ''

    def exists(self):
        return self.db.exists(self.group)
    
    def kw_exists(self):
        return self.db.exists(self.get_kw_db())

    def kw_all_exists(self):
        return self.db.exists(self.get_all_kw_db())
    
    def get_kw_db(self):
        return self.group + '-kw'

    def get_all_kw_db(self):
        return self.group + '-al'
# -*- coding: utf-8 -*-
from .abstract import AbstractPermisson


class UserRelate(AbstractPermisson):
    category = '用户相关'
    perms = [
        {
            'codename': 'editor_user',
            'name': '修改用户',
        },
        {
            'codename': 'get_user_info',
            'name': '获取用户信息',
        },
    ]


class BookOperate(AbstractPermisson):
    perms = [
        {
            'codename': 'delete_book',
            'name': '删除书籍',
        },
    ]

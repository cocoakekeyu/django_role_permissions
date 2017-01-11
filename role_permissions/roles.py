# -*- coding: utf-8 -*-
from role_permissions.abstract import AbstractRole


class Doctor(AbstractRole):
    permissions = [
        'Can_operate_suit',
        'Can_update_suit',
    ]


class Nurse(AbstractRole):
    name = '护士'
    permissions = [
        'Can_operate_suit',
    ]


class JJJJJJ(AbstractRole):
    permissions = [
        'Can_operate_suit',
    ]

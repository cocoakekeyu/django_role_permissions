# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.test import TestCase
from model_mommy import mommy

from role_permissions.abstract import AbstractRole
from role_permissions.shortcut import (
    add_role, get_user_role,
)
from role_permissions.utils import get_role_model


class Role1(AbstractRole):
    permissions = [
        'Can_do_something',
    ]


class Role2(AbstractRole):
    name = 'Ciline'
    permissions = [
        'Can_operate_hello',
    ]


class Role3(AbstractRole):
    name = 'Worker'
    permissions = [
        'Can_update_machine',
        'Can_operate_machine',
    ]


class AssignRole(TestCase):

    def setUp(self):
        self.user = mommy.make(get_user_model())

    def _test_add_role(self):
        user = self.user
        print(user.username)
        add_role(user, Role1)
        print(Role1.get_registered_role().group.user_set.all()[0].username)
        self.assertEqual(get_user_role(user), Role1.get_registered_role()) #.get_registered_role())

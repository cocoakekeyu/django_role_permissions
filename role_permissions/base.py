# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group


class AbstractBaseRole(models.Model):
    group = models.OneToOneField(Group, models.CASCADE, primary_key=True)
    name = models.CharField('角色名称', max_length=80, unique=True)
    is_active = models.BooleanField('状态', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'auth_role'

    def __str__(self):
        return self.name

    @property
    def id(self):
        return self.group.id

    # @property
    # def name(self):
    #     return self.group.name

    # @name.setter
    # def name(self, value):
    #     self.group.name = value

    @property
    def permissions(self):
        return self.group.permissions

    def assign_role_to_user(self, user):
        user = getattr(user, 'user', None) or user
        self.group.user_set.add(user)

    def as_group(self):
        return self.group

    def save(self, *args, **kwargs):
        self.group.save()
        super(AbstractBaseRole, self).save(*args, **kwargs)

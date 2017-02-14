# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group


class AbstractBaseRole(models.Model):
    group = models.OneToOneField(Group, models.CASCADE)
    name = models.CharField('角色名称', max_length=80, unique=True)
    is_active = models.BooleanField('状态', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        db_table = 'auth_role'

    def __str__(self):
        return self.name

    @property
    def permissions(self):
        return self.group.permissions

    def assign_role_to_user(self, user):
        # self.group.user_set.add(user)
        user.groups.add(self.group)

    def as_group(self):
        return self.group

    def save(self, *args, **kwargs):
        self.group.name = self.name
        self.group.save()
        super(AbstractBaseRole, self).save(*args, **kwargs)

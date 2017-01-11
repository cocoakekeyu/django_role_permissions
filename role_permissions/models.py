# -*- coding: utf-8 -*-
from .base import AbstractBaseRole
from django.db import models
from django.contrib.auth.models import Group, Permission


class RoleManage(models.Manager):
    def create(self, name, permissions=None, **extra_fields):
        group, created = Group.objects.get_or_create(name=name)
        if permissions:
            group.permissions.set(permissions)
        role = self.model(group=group, name=name, **extra_fields)
        role.save(using=self._db)

        return role

    def get_queryset(self):
        return super(RoleManage, self).get_queryset().prefetch_related('group')


class Role(AbstractBaseRole):
    objects = RoleManage()


class PermissionGroup(models.Model):
    permission = models.OneToOneField(
        Permission, models.CASCADE, primary_key=True, related_name='category')
    name = models.CharField('权限分组', max_length=80, default='default')

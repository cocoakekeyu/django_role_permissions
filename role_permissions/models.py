# -*- coding: utf-8 -*-
from .base import AbstractBaseRole
from django.db import models
from django.contrib.auth.models import Group


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

    # def get(self, *args, **kwargs):
    #     name = kwargs.pop('name', None)
    #     if name:
    #         kwargs['group__name'] = name

    #     return super(RoleManage, self).get(*args, **kwargs)

    # def get_or_create(self, defaults=None, **kwargs):
    #     lookup, params = self._extract_model_params(defaults, **kwargs)
    #     self._for_write = True
    #     try:
    #         return self.get(**lookup), False
    #     except self.model.DoesNotExist:
    #         return self._create_object_from_params(lookup, params)
    #     return super(RoleManage, self).get_or_create(defaults, **kwargs)


class Role(AbstractBaseRole):
    objects = RoleManage()

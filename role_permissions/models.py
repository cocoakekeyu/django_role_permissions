# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import Group


class RoleManage(models.Manager):
    def create(self, name, permissions=None, **extra_fields):
        group, created = Group.objects.get_or_create(name=name)
        if permissions:
            group.permissions.set(permissions)
        role = self.model(group=group, **extra_fields)
        role.save(using=self._db)

        return role

    def get_queryset(self):
        return super(RoleManage, self).get_queryset().prefetch_related('group')


class Role(models.Model):
    group = models.OneToOneField(Group, models.CASCADE, primary_key=True)
    is_active = models.BooleanField('状态', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    objects = RoleManage()

    class Meta:
        db_table = 'auth_role'

    def __str__(self):
        return self.name

    @property
    def id(self):
        return self.group.id

    @property
    def name(self):
        return self.group.name

    @name.setter
    def name(self, value):
        self.group.name = value

    @property
    def permissions(self):
        return self.group.permissions

    def assign_role_to_user(self, user):
        user = getattr(user, 'user', None) or user
        self.group.user_set.add(user)

    def save(self, *args, **kwargs):
        self.group.save()
        super(Role, self).save(*args, **kwargs)

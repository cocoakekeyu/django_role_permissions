# -*- coding: utf-8 -*-
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


class AbstractBaseRole(models.Model):
    group = models.OneToOneField(Group, models.CASCADE)
    name = models.CharField('角色名称', max_length=80, unique=True)
    is_active = models.BooleanField('状态', default=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    objects = RoleManage()

    class Meta:
        db_table = 'auth_role'
        abstract = True

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


class Role(AbstractBaseRole):
    pass


class PermissionGroup(models.Model):
    permission = models.OneToOneField(
        Permission, models.CASCADE, primary_key=True, related_name='category')
    name = models.CharField('权限分组', max_length=80, default='default')

# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist
from .models import Role


class RoleInputSerializer(serializers.ModelSerializer):
    """
    创建或修改角色的序列化器
    """
    name = serializers.CharField(
        label='名称', max_length=32,
        validators=[UniqueValidator(
            queryset=Group.objects.all(), message='角色名称已存在')])
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )

    class Meta:
        model = Role
        exclude = ('group',)
        read_only_fields = ('create_time',)

    def update(self, instance, validated_data):
        permission_codenames = validated_data.pop('permissions', None)
        if permission_codenames:
            permissions = Permission.objects.filter(
                codename__in=permission_codenames)
            if len(permissions) < len(permission_codenames):
                raise ObjectDoesNotExist('未找到对应的权限')
            instance.permissions.set(permissions, clear=True)
        return super(
            RoleInputSerializer, self).update(instance, validated_data)


class RoleOutputSerializer(serializers.ModelSerializer):
    """
    角色序列化器
    """
    id = serializers.IntegerField(
        label='ID', source='group_id', read_only=True)
    name = serializers.CharField(label='名称', max_length=255)
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )

    class Meta:
        model = Role
        exclude = ('group',)

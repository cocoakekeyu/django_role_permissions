# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Role
from .shortcut import get_permissions
from .__init__ import get_role_model


class RoleInputSerializer(serializers.ModelSerializer):
    """
    创建或修改角色的序列化器
    """
    name = serializers.CharField(
        label='名称', max_length=80,
        validators=[UniqueValidator(
            queryset=get_role_model().objects.all(), message='角色名称已存在')])
    permissions = serializers.ListField(
        child=serializers.CharField(max_length=255)
    )

    class Meta:
        model = Role
        exclude = ('group',)
        read_only_fields = ('create_time',)

    def create(self, validated_data):
        permission_codenames = validated_data.pop('permissions', None)
        if permission_codenames:
            permissions = get_permissions(permission_codenames)
            validated_data['permissions'] = permissions
        return super(
            RoleInputSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        permission_codenames = validated_data.pop('permissions', None)
        if permission_codenames:
            permissions = get_permissions(permission_codenames)
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

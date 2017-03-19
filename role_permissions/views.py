# -*- coding: utf-8 -*-
from operator import attrgetter
import itertools

from django.views import View
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.views import APIView
from rest_framework.response import Response

from role_permissions import get_role_model
from .shortcut import get_all_permissions, get_user_permissions
from .serializer import PermissionSerializer, PermissionGroupSerializer


class PermissionView(APIView):

    def get(self, request):
        """
        获取所有角色权限
        """
        role_ct = ContentType.objects.get_for_model(get_role_model())
        permissions = Permission.objects.filter(content_type=role_ct).exclude(
            name__startswith='Can').prefetch_related('category')
        permissions = list(permissions)
        permissions.sort(key=attrgetter('category.name'))
        permission_groups = []
        for k, v in itertools.groupby(permissions, key=attrgetter('category.name')):
            permission_group = {}
            permission_group['category'] = k
            permission_group['permissions'] = list(v)
            permission_groups.append(permission_group)

        serializer = PermissionGroupSerializer(permission_groups, many=True)
        return Response(serializer.data)


class UserPermissionView(APIView):

    def get(self, request, userid):
        """
        获取用户权限
        """
        User = get_user_model()
        user = User.objects.get(id=userid)
        permissions = get_user_permissions(user)
        serializer = PermissionSerializer(permissions, many=True)
        return Response(serializer.data)


class RoleView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass


class RoleDetailView(View):

    def get(self, request, pk):
        pass

    def delete(self, request, pk):
        pass

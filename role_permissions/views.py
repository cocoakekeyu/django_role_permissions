# -*- coding: utf-8 -*-
from django.views import View
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response

from .shortcut import get_all_permissions, get_user_permissions
from .serializer import PermissionSerializer


class PermissionView(APIView):

    def get(self, request):
        """
        获取所有角色权限
        """
        permissions = get_all_permissions()
        serializer = PermissionSerializer(permissions, many=True)
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

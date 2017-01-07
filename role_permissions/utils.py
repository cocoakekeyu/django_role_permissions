# -*- coding: utf-8 -*-
from .models import Role


def assign_roles(user, roles):
    remove_roles(user)
    for role in roles:
        role.assign_role_to_user(user)


def remove_role(user, role):
    """
    移除用户角色
    """
    user = getattr(user, 'user', None) or user
    user.groups.clear()


def remove_roles(user):
    """
    移除用户所有角色
    """
    user = getattr(user, 'user', None) or user
    user.groups.clear()


def has_role(user, role):
    if user in role.group.user_set:
        return True
    return False


def get_user_roles(user):
    """
    获取用户所有角色
    """
    user = getattr(user, 'user', None) or user
    roles = Role.objects.filter(group__in=user.groups.all())
    return list(roles)


def get_user_role(user):
    """
    获取用户一个角色
    """
    roles = get_user_roles(user)
    return roles[0] if roles else None

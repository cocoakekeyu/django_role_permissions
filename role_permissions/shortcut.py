# -*- coding: utf-8 -*-
from .models import Role
from django.apps import apps as django_apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# Role operate

def assign_roles(user, roles):
    """
    给用户分配角色
    """
    remove_roles(user)
    for role in roles:
        role.assign_role_to_user(user)


def add_role(user, role):
    """
    给用户添加一个角色
    """
    user = getattr(user, 'user', None) or user
    if user in role.group.user_set:
        return
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


def get_role_model():
    """
    Returns the Role model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_ROLE_MODEL)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'")
    except (LookupError, AttributeError):
        return Role

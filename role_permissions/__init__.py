# -*- coding: utf-8 -*-
from django.conf import settings
from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

default_app_config = 'role_permissions.apps.RolePermissionsConfig'


def get_role_model():
    """
    Returns the Role model that is active in this project.
    """
    try:
        return django_apps.get_model(settings.AUTH_ROLE_MODEL)
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_ROLE_MODEL must be of the form 'app_label.model_name'")
    except (LookupError, AttributeError):
        from .models import Role
        return Role

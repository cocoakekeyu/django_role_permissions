from importlib import import_module

from django.apps import AppConfig
from django.conf import settings


class SimpleConfig(AppConfig):
    name = 'role_permissions'


class RolePermissionsConfig(AppConfig):
    name = 'role_permissions'

    def ready(self):
        self.init_permissions()

    def init_permissions(self):
        permissions_module = getattr(settings, 'ROLE_PERMISSIONS_MODULE', None)
        if permissions_module:
            import_module(permissions_module)
        else:
            from django.apps import apps
            for app_config in apps.get_app_configs():
                try:
                    import_module('%s.permissions' % app_config.name)
                except:
                    pass

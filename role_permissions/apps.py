import logging
from importlib import import_module

from django.apps import AppConfig
from django.conf import settings
from django.db.utils import OperationalError


logger = logging.getLogger(__name__)


class SimpleConfig(AppConfig):
    name = 'role_permissions'


class RolePermissionsConfig(AppConfig):
    name = 'role_permissions'

    def ready(self):
        self.init_permissions()

    def init_permissions(self):
        from django.contrib.contenttypes.models import ContentType
        from .models import PermissionGroup
        try:
            ContentType.objects.get_for_model(PermissionGroup)
        except OperationalError:
            logger.warning('ContentType app not migrate')
        except RuntimeError:
            logger.warning('application migrations not apply')
        else:
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

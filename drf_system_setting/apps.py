from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

__all__ = ["DrfSysSettingConfig"]


class DrfSysSettingConfig(AppConfig):
    """Default configuration for django_celery_beat app."""

    name = "drf_system_setting"
    label = "drf_system_setting"
    verbose_name = _("系统设置")
    default_auto_field = "django.db.models.BigAutoField"

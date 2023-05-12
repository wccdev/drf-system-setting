from django.db import models
from drfexts import fields

from ..choices import MenuTypeChoices
from ..core.models import BaseSettingModel, TreePathMixin


class MenuQuerySet(models.QuerySet):
    # def menus(self):
    #     return self.filter(type=MenuTypeChoices.MENU)
    #
    # def pages(self):
    #     return self.filter(type=MenuTypeChoices.PAGE)

    @property
    def menus(self):
        return self.exclude(type=MenuTypeChoices.BUTTON)

    @property
    def buttons(self):
        return self.filter(type=MenuTypeChoices.BUTTON)


class Menu(BaseSettingModel, TreePathMixin):
    hidden = fields.BooleanField("隐藏", default=False)
    keep_alive = fields.BooleanField("缓存", default=True)
    is_link = fields.BooleanField("是否连接", default=False)
    icon = fields.CharField("图标", max_length=50, blank=True, default="")
    component = fields.CharField("组件路径", max_length=100, blank=True, default="")
    path = fields.CharField("路径", max_length=256, null=True, default="")
    redirect = fields.TextField("重定向", max_length=256, null=True, default="")
    type = fields.SmallIntegerField("类型", choices=MenuTypeChoices.choices, default=MenuTypeChoices.MENU)

    objects = MenuQuerySet.as_manager()

    def __str__(self):
        return self.name

    @property
    def perm_name(self):
        return self.name

    @property
    def perm_code(self):
        # return f"{self.system.code}-{self.code}"
        return self.code

    # @property
    # def perm_show_name(self):
    #     return self.show_name

    class Meta:
        managed = True
        # db_table = 'setting"."menu'
        verbose_name = verbose_name_plural = "菜单"
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "name"],
                # condition=Q(status__in=[RbacCommonStatus.ENABLE, RbacCommonStatus.DISABLE]),
                name="unique_setting_menu_name"
            ),
            models.UniqueConstraint(
                fields=["parent", "code"],
                name="unique_setting_menu_code"
            )
        ]

from django.db.models import UniqueConstraint
from drfexts import fields

from ..choices import DictTypeChoices
from ..core.models import BaseSettingModel, TreePathMixin


class Dict(BaseSettingModel, TreePathMixin):
    code = fields.CharField("编号", max_length=100)
    type = fields.SmallIntegerField("类型", choices=DictTypeChoices.choices, default=DictTypeChoices.INT)
    # ext_field1 = fields.CharField("Ext1", max_length=100, blank=True, default="")
    # ext_field2 = fields.CharField("Ext2", max_length=100, blank=True, default="")
    # ext_field3 = fields.CharField("Ext3", max_length=100, blank=True, default="")
    # ext_field4 = fields.CharField("Ext4", max_length=100, blank=True, default="")
    # ext_field5 = fields.CharField("Ext5", max_length=100, blank=True, default="")

    class Meta:
        managed = True
        # db_table = 'setting"."dict'
        verbose_name = verbose_name_plural = "字典"
        constraints = [
            UniqueConstraint(fields=["parent", "name"], name="unique_setting_dict_name"),
            UniqueConstraint(fields=["parent", "code"], name="unique_setting_dict_code")
        ]

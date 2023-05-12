from drfexts import fields
from drfexts.models import BaseCreatorModel


class BaseSettingModel(BaseCreatorModel):
    sort = fields.IntegerField("排序", null=True)
    code = fields.CharField("编号", max_length=100, unique=True)
    name = fields.CharField("名称", max_length=50)
    parent = fields.VirtualForeignKey("父级", to="self", null=True, related_name="children")
    # status = fields.CharField("状态", max_length=50, blank=True, default="")
    # stable = fields.CharField("内置", max_length=50, blank=True, default="")
    stable = fields.BooleanField("内置", default=False)
    description = fields.CharField("描述", max_length=255, blank=True, default="")

    class Meta:
        abstract = True


class TreePathMixin:
    @property
    def _tree_path(self):
        path = [self.name]

        c = self
        while True:
            parent = c.parent
            if parent:
                path.insert(0, parent.name)
                c = parent
            else:
                break
        return path

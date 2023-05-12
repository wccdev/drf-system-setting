from django.db.models import IntegerChoices


class MenuTypeChoices(IntegerChoices):
    MENU = 1, "菜单"
    PAGE = 2, "页面"
    BUTTON = 3, "按钮"


class DictTypeChoices(IntegerChoices):
    INT = 1, "整数"
    STR = 2, "字符串"
    BOOL = 3, "布尔值"

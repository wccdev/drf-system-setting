from django.db.models import F, Prefetch
from drfexts.choices import SimpleStatus
from drfexts.serializers.serializers import WCCModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import APIException

from .core.serializers import CustomDisplayChoiceField, ListTreePathSerializer
from .models import Dict, Menu


class BaseSerializer(WCCModelSerializer):
    status = CustomDisplayChoiceField(choices=SimpleStatus.choices)
    tree_path = serializers.ListField(read_only=True, default=[])
    parent_code = serializers.CharField(default="", required=False, allow_null=True, allow_blank=True)

    def set_parent(self, instance, validated_data):
        parent_code = validated_data.pop("parent_code", "")
        if parent_code:
            try:
                parent = self.Meta.model.objects.get(code=parent_code)
            except Exception:
                raise APIException(f"父级元素不存在, code: {parent_code}")
            if parent.pk == instance.id:
                raise APIException("无法设置数据自己为父级！")
            instance.parent = parent
            instance.save()

    def create(self, validated_data):
        instance = super().create(validated_data)
        self.set_parent(instance, validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        self.set_parent(instance, validated_data)
        return instance

    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     if not ret["tree_path"]:
    #         ret["tree_path"] = instance._tree_path
    #     return ret


class DictSerializer(BaseSerializer):
    parent_id = serializers.IntegerField(default=None, allow_null=True)

    @classmethod
    def process_queryset(cls, request, queryset):
        return (
            queryset.filter(status=SimpleStatus.VALID)
            .annotate(parent_code=F("parent__code"))
            .select_related("parent", "created_by", "updated_by")
        )

    class Meta:
        model = Dict
        exclude = ["parent", ]
        list_serializer_class = ListTreePathSerializer


class DictRetrieveSerializer(DictSerializer):
    tree_path = serializers.ListField(source="_tree_path", read_only=True, default=[])


class ButtonSerializer(serializers.ModelSerializer):
    parent_id = serializers.IntegerField(default=None, read_only=True)
    parent_code = serializers.CharField(default="", read_only=True)
    parent_name = serializers.CharField(default="", read_only=True)

    @classmethod
    def process_queryset(cls, request, queryset):
        return queryset.buttons.annotate(parent_code=F("parent__code"), parent_name=F("parent__name")).order_by("sort")

    class Meta:
        model = Menu
        fields = ["id", "code", "name", "parent_id", "parent_code", "parent_name"]


class MenuSerializer(BaseSerializer):
    parent_id = serializers.IntegerField(default=None, allow_null=True)
    # parent_code = serializers.CharField(default="", read_only=True)
    buttons = ButtonSerializer(many=True, read_only=True)
    path = serializers.CharField(allow_blank=True)
    redirect = serializers.CharField(allow_blank=True)

    @classmethod
    def process_queryset(cls, request, queryset):
        return (
            queryset.menus
            .annotate(
                parent_code=F("parent__code"),
                # created_by_name=F("created_by__username"),
                # updated_by_name=F("updated_by__username"),
            )
            .select_related("created_by", "updated_by")
            .prefetch_related(
                Prefetch(
                    "children",
                    queryset=queryset.buttons.order_by("sort"),
                    to_attr="buttons",
                )
            )
        )

    class Meta:
        model = Menu
        exclude = ["parent", ]
        list_serializer_class = ListTreePathSerializer


class MenuRetrieveSerializer(MenuSerializer):
    tree_path = serializers.ListField(source="_tree_path", read_only=True, default=[])

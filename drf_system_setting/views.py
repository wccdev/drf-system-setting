from drfexts.viewsets import ExtGenericViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from .models import Dict, Menu
from .serializers import (
    ButtonSerializer,
    DictRetrieveSerializer,
    DictSerializer,
    MenuRetrieveSerializer,
    MenuSerializer,
)


class DictViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    ExtGenericViewSet,
):
    queryset = Dict.objects.all()
    serializer_class = {
        "default": DictSerializer,
        "create": DictRetrieveSerializer,
        "update": DictRetrieveSerializer,
        "retrieve": DictRetrieveSerializer
    }

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.stable:
            raise APIException(detail="内置字典不能删除！")
        self.queryset.filter(parent=instance).delete()
        self.perform_destroy(instance)
        return Response()


class MenuViewSet(
    ListModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    ExtGenericViewSet
):
    queryset = Menu.objects.all()
    serializer_class = {
        "default": MenuSerializer,
        "retrieve": MenuRetrieveSerializer,
        "buttons": ButtonSerializer,
    }
    ordering = ("sort", )

    @action(detail=True)
    def buttons(self, request, pk, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset().filter(parent_id=pk), many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.stable:
            raise APIException(detail="内置内容不能删除！")
        parent_ids = [instance.id]
        delete_ids = []
        while True:
            children_ids = list(self.queryset.filter(parent_id__in=parent_ids).values_list("id", flat=True))
            if children_ids:
                delete_ids.extend(children_ids)
                parent_ids = children_ids
            else:
                break
        self.queryset.filter(id__in=delete_ids).delete()
        self.perform_destroy(instance)
        return Response()

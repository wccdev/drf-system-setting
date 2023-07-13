from rest_framework.routers import SimpleRouter

from .views import DictViewSet, MenuViewSet

router = SimpleRouter()

app_name = "drf_system_setting"

router.register("dicts", DictViewSet)
router.register("menus", MenuViewSet)

urlpatterns = router.urls

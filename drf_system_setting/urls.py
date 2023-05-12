from rest_framework.routers import SimpleRouter

from .views import DictViewSet, MenuViewSet

router = SimpleRouter()

router.register("dicts", DictViewSet)
router.register("menus", MenuViewSet)

urlpatterns = router.urls

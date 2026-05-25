from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TenantViewSet, DataSourceViewSet, DataUploadViewSet, ActivityDataViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)
router.register(r'sources', DataSourceViewSet)
router.register(r'uploads', DataUploadViewSet)
router.register(r'activities', ActivityDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

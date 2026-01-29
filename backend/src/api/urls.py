from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquipmentViewSet, FileUploadViewSet

router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'upload', FileUploadViewSet, basename='upload')

urlpatterns = [
    path('v1/', include(router.urls)),
]

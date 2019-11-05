# API url configuration

from api import views
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register(r'entry', views.EntryViewSet)

urlpatterns = [
  path('', include(router.urls)),
]
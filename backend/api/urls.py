# API url configuration

from api import views
from rest_framework.routers import SimpleRouter
from django.urls import path, include
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
	TokenVerifyView
)
router = SimpleRouter()
router.register('users', views.UserViewSet)
router.register('records', views.RecordViewSet)

urlpatterns = [
	path('login/', views.LoginView.as_view()),
	path('signup/', views.RegisterView.as_view()),
	path('token/', TokenObtainPairView.as_view(), name='token'),
	path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),		   # refresh token for simple jwt
	path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),			  # verifying token for simple jwt 
	path('', include(router.urls)),
]
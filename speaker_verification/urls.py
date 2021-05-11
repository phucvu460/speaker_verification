from django.urls import path, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from speaker_verification.api import UserModelViewSet, Predict
from . import views


router = DefaultRouter()
router.register(r'user', UserModelViewSet, basename='user-api')

urlpatterns = [
    path("", views.index, name="index"),
    path(r'api/v1/', include(router.urls)),
    path('speaker-verify', Predict.as_view())
    # path('register/', views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
]

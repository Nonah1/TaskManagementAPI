from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, UserViewSet, NotificationViewSet

#creates endpoints for viewsets automaticalyy
router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'users', UserViewSet, basename='user')
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
 

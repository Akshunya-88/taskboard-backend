from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, CategoryViewSet,dashboard_view,advice_view

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'', TaskViewSet, basename='task')

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('advice/', advice_view, name='advice'),
    path('', include(router.urls)),
]

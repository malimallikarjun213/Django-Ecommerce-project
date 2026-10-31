
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CategoryViewSet, category_detail
from.import views
router = DefaultRouter()
router.register('categories', CategoryViewSet, basename='category')

urlpatterns = [
    path(
        'category/<int:category_id>/',
        category_detail,
        name='category_detail'
    ),
]

urlpatterns += router.urls

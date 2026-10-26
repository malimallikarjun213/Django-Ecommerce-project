
from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),

    path(
        'category/<int:category_id>/',
        views.category_products,
        name='category_products'
    ),

    path(
        'product/<int:id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'product/<int:id>/review/',
        views.add_review,
        name='add_review'
    ),

    path('api/', views.ProductListAPI.as_view(), name='product_api'),

    path(
        'add-to-cart/<int:id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path('cart/', views.cart_view, name='cart'),
]

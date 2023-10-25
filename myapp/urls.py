from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='home'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('product-detail/<int:pk>',views.product_detail,name='product-detail'),
    path('add-product/', views.add_product, name='add-product'),
    path('update-product/<int:pk>/', views.update_product, name='update-product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete-product'),
    path('user-index/',views.user_index,name='user-index'),
    path('user-product-details/<int:pk>',views.user_product_details,name='user-product-details'),
    path('update_price/<int:pk>/', views.update_price, name='update_price'),
]
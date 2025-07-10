from django.contrib import admin
from django.urls import path,include
from .  import views
from .views import delete_user

urlpatterns = [
   path('1',views.home),
   path('2',views.about),
   path('3',views.user_login),
   path('4',views.register),
   path('5', views.viewusers),
   path('6', views.edit),
   path('8', views.products),
   
   path("delete/<int:user_id>", delete_user, name="delete_user"),
   path("edit/<int:user_id>",views.edit_user),
   path('logout/', views.logout_view, name='logout'),
   path('edit/<int:product_id>/', views.edit_product, name='edit_product'),
   path('delete/<int:product_id>/', views.delete_product, name='delete_product'),
   path('9', views.view_products, name='product_list'),
   path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
   path('10', views.view_cart, name='view_cart'),
   path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
   path('11', views.buy_product, name='buy'),
   path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
   path('buy/<int:product_id>/', views.buy_product, name='buy_product'),
   path('orders/', views.view_orders, name='view_orders'),
   path('bookings/', views.view_bookings, name='view_bookings'),  
   path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
   path('checkout/', views.checkout_cart, name='checkout_cart'),
   path('buy-all/', views.buy_all_view, name='buy_all_view'),
   path('confirm-buy/', views.confirm_buy_all, name='confirm_buy_all'),
   path('update-status/<int:order_id>/', views.update_order_status, name='update_order_status'),
   path('submit-feedback/<int:order_id>/', views.submit_feedback, name='submit_feedback'),
   path('delete-category/<int:category_id>/', views.delete_category, name='delete_category'),


   path('add-category/', views.add_category, name='add_category'),
   path('add-product/', views.add_product, name='add_product'),
   path('cart/update/<int:product_id>/', views.update_cart_quantity, name='update_cart_quantity'),
]

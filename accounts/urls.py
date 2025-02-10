from django.urls import path

from . import views
urlpatterns = [
    path('signup', views.signup, name='accounts.signup'),
    path('login', views.login, name='accounts.login'),
    path('logout/', views.logout, name='accounts.logout'),
    path('orders/', views.orders, name='accounts.orders'),
    path('request_reset/', views.request_reset, name='accounts.request_reset'),
    path('reset_password/<str:username>/', views.reset_password, name='accounts.reset_password'),
]
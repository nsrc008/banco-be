from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from authApp import views

urlpatterns = [
    path('login/',      TokenObtainPairView.as_view()),
    path('refresh/',    TokenRefreshView.as_view()),
    path('user/',       views.UserCreateView.as_view()),
    path('user/<int:pk>/', views.UserDetailView.as_view()),
    path('transaccion/create',       views.UserCreateView.as_view()),
    path('transaccion/<int:user>/<int:pk>/', views.UserDetailView.as_view()),
    path('transaccion/update/<int:user>/<int:pk>/',       views.UserCreateView.as_view()),
    path('transaccion/remove/<int:user>/<int:pk>/', views.UserDetailView.as_view()),
    path('transaccion/<int:user>/<int:account>/',       views.UserCreateView.as_view()),
    
]
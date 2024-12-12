from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'tracker'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.user_logout, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', views.category_list, name='category_list'),
    path('create/', views.category_create, name='category_create'),
    path('update/<int:category_id>/', views.category_update, name='category_update'),
    path('delete/<int:category_id>/', views.category_delete, name='category_delete'),
]

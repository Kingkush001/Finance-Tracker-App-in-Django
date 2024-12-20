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

    path('category', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('update/<int:category_id>/', views.category_update, name='category_update'),
    path('delete/<int:category_id>/', views.category_delete, name='category_delete'),

    path('budget', views.budget_list, name='budget_list'),
    path('<int:pk>/', views.budget_detail, name='budget_detail'),
    path('budget/create/', views.budget_create, name='budget_create'),
    path('<int:pk>/edit/', views.budget_update, name='budget_update'),
    path('<int:pk>/delete/', views.budget_delete, name='budget_delete'),

    path("debt/", views.debt_list, name="debt_list"),
    path("<int:debt_id>/", views.debt_detail, name="debt_detail"),
    path("debt/create/", views.debt_create, name="debt_create"),
    path("<int:debt_id>/update/", views.debt_update, name="debt_update"),
    path("<int:debt_id>/delete/", views.debt_delete, name="debt_delete"),

    path('savings/', views.savings_list, name='savings_list'),
    path('create/', views.savings_create, name='savings_create'),
    path('update/<int:savings_id>/', views.savings_update, name='savings_update'),
    path('delete/<int:savings_id>/', views.savings_delete, name='savings_delete'),

    path('reports/', views.report_list, name='report_list'),
    path('reports/<int:report_id>/download/csv/', views.download_report_csv, name='download_report_csv'),
    path('reports/<int:report_id>/download/pdf/', views.download_report_pdf, name='download_report_pdf'),
    path('generate-report/', views.generate_report_view, name='generate_report'),

    path('currencies/', views.currency_list, name='currency_list'),
    path('currencies/<int:currency_id>/', views.currency_detail, name='currency_detail'),
    path('currencies/add/', views.add_currency, name='add_currency'),
    path('currencies/download_csv/', views.download_currencies_csv, name='download_currencies_csv'),

    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/new/', views.transaction_create, name='transaction_create'),
    path('transactions/edit/<int:transaction_id>/', views.transaction_edit, name='transaction_edit'),

    path('recurring/', views.recurring_list, name='recurring_list'),
    path('recurring/create/', views.recurring_create, name='recurring_create'),
    path('recurring/edit/<int:recurring_id>/', views.recurring_edit, name='recurring_edit'),
    path('recurring/delete/<int:recurring_id>/', views.recurring_delete, name='recurring_delete'),
]


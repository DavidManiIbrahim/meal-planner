from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/setup/', views.profile_setup_view, name='profile_setup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
path('generate-plan/', views.generate_plan_view, name='generate_plan'),
path('shopping-list/', views.shopping_list_view, name='shopping_list'),
path('rate-dish/', views.rate_dish_view, name='rate_dish'),
]
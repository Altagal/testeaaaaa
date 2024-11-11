from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts import views

urlpatterns = [
    path('', views.account_login, name='account_login'),
    path('sair', views.account_logout, name='account_logout'),
    path('registrar-se', views.account_register, name='account_register'),
    path('home', views.home, name='home'),

    path('contas', views.account_list, name='account_list'),
    # path('ver-usuario/<str:pk>/', views.account_read, name='account_read'), # nao ultilizado
    path('conta/<str:pk>/', views.account_update, name='account_update'),
    path('excluir-conta/<str:pk>/', views.account_delete, name='account_delete'),

    path('resetar-senha-conta/<str:pk>/', views.account_reset_password, name='account_reset_password'),
    path('trocar-senha-conta', views.account_change_password, name='account_change_password'),

    path('grupos', views.group_list, name='group_list'),
    # path('ver-grupo/<str:pk>/', views.group_read, name='group_user'), # nao ultilizado
    path('cadastrar-grupo', views.group_create, name='group_create'),
    path('editar-grupo/<str:pk>/', views.group_update, name='group_update'),
    path('excluir-grupo/<str:pk>/', views.group_delete, name='group_delete'),
]

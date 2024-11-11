from django.urls import path, include

from foos import views

urlpatterns = [
    path('foos', views.foo_list, name='foo_list'),
    path('cadastrar-foo', views.foo_create, name='foo_create'),
    path('editar-foo/<str:pk>/', views.foo_update, name='foo_update'),
    path('excluir-foo/<str:pk>/', views.foo_delete, name='foo_delete'),

]

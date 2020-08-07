from django.urls import path

from account.login import views

urlpatterns = [
    path('create', views.Create.as_view(), name='create'),
    path('delete/<int:pk>', views.Delete.as_view(), name='delete'),
    path('password', views.Password.as_view(), name='password'),
    path('permission/<int:pk>', views.Permission.as_view(), name='permission'),
    path('permission/base', views.BasePermissions.as_view(), name='permission-base'),
    path('permission/user', views.UserPermission.as_view(), name='permission-user')
]

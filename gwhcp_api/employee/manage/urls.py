from django.urls import path

from employee.manage import views

urlpatterns = [
    path(
        'accesslog/<int:pk>',
        views.AccessLog.as_view(),
        name='accesslog'
    ),

    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        'delete/<int:pk>',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        'permission/<int:pk>',
        views.Permission.as_view(),
        name='permission'
    ),

    path(
        'permission/base',
        views.PermissionBase.as_view(),
        name='permission-base'
    ),

    path(
        'permission/user',
        views.PermissionUser.as_view(),
        name='permission-user'
    ),

    path(
        'profile/<int:pk>',
        views.Profile.as_view(),
        name='profile'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

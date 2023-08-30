from django.urls import path

from admin.employee.manage import views

urlpatterns = [
    path(
        '<int:pk>/accesslog',
        views.AccessLog.as_view(),
        name='accesslog'
    ),

    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        '<int:pk>/delete',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        '<int:pk>/permission',
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
        'search',
        views.Search.as_view(),
        name='search'
    )
]

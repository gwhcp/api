from django.urls import path

from client.account import views

urlpatterns = [
    path(
        'accesslog',
        views.AccessLog.as_view(),
        name='accesslog'
    ),

    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        'edit',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        'password',
        views.Password.as_view(),
        name='password'
    ),

    path(
        'permission/user',
        views.PermissionUser.as_view(),
        name='permission-user'
    )
]

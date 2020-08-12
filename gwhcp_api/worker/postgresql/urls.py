from django.urls import path

from worker.postgresql import views

app_name = 'postgresql'

urlpatterns = [
    path(
        'create/database',
        views.CreateDatabase.as_view(),
        name='create-database'
    ),

    path(
        'create/user',
        views.CreateUser.as_view(),
        name='create-user'
    ),

    path(
        'delete/database',
        views.DeleteDatabase.as_view(),
        name='delete-database'
    ),

    path(
        'delete/user',
        views.DeleteUser.as_view(),
        name='delete-user'
    ),

    path(
        'disable',
        views.Disable.as_view(),
        name='disable'
    ),

    path(
        'enable',
        views.Enable.as_view(),
        name='enable'
    ),

    path(
        'password',
        views.Password.as_view(),
        name='password'
    ),

    path(
        'permission',
        views.Permission.as_view(),
        name='permission'
    ),

    path(
        'server/install',
        views.ServerInstall.as_view(),
        name='server-install'
    ),

    path(
        'server/uninstall',
        views.ServerUninstall.as_view(),
        name='server-uninstall'
    )
]

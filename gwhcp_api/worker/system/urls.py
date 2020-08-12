from django.urls import path

from worker.system import views

app_name = 'system'

urlpatterns = [
    path(
        'create/group',
        views.CreateGroup.as_view(),
        name='create-group'
    ),

    path(
        'create/group/quota',
        views.CreateGroupQuota.as_view(),
        name='create-group-quota'
    ),

    path(
        'create/host',
        views.CreateHost.as_view(),
        name='create-host'
    ),

    path(
        'create/hostname',
        views.CreateHostname.as_view(),
        name='create-hostname'
    ),

    path(
        'create/ipaddress',
        views.CreateIpaddress.as_view(),
        name='create-ipaddress'
    ),

    path(
        'create/user',
        views.CreateUser.as_view(),
        name='create-user'
    ),

    path(
        'create/user/quota',
        views.CreateUserQuota.as_view(),
        name='create-user-quota'
    ),

    path(
        'delete/group',
        views.DeleteGroup.as_view(),
        name='delete-group'
    ),

    path(
        'delete/host',
        views.DeleteHost.as_view(),
        name='delete-host'
    ),

    path(
        'delete/hostname',
        views.DeleteHostname.as_view(),
        name='delete-hostname'
    ),

    path(
        'delete/ipaddress',
        views.DeleteIpaddress.as_view(),
        name='delete-ipaddress'
    ),

    path(
        'delete/user',
        views.DeleteUser.as_view(),
        name='delete-user'
    )
]

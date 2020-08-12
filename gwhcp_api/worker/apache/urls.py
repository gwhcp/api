from django.urls import path

from worker.apache import views

app_name = 'apache'

urlpatterns = [
    path(
        'create/config',
        views.CreateConfig.as_view(),
        name='create-config'
    ),

    path(
        'delete/config',
        views.DeleteConfig.as_view(),
        name='delete-config'
    ),

    path(
        'disable/domain',
        views.DisableDomain.as_view(),
        name='disable-domain'
    ),

    path(
        'enable/domain',
        views.EnableDomain.as_view(),
        name='enable-domain'
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

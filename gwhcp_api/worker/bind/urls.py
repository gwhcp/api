from django.urls import path

from worker.bind import views

app_name = 'bind'

urlpatterns = [
    path(
        'create/domain',
        views.CreateDomain.as_view(),
        name='create-domain'
    ),

    path(
        'delete/domain',
        views.DeleteDomain.as_view(),
        name='delete-domain'
    ),

    path(
        'rebuild/all',
        views.RebuildAll.as_view(),
        name='rebuild-all'
    ),

    path(
        'rebuild/domain',
        views.RebuildDomain.as_view(),
        name='rebuild-domain'
    ),

    path(
        'reload/domain',
        views.ReloadDomain.as_view(),
        name='reload-domain'
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

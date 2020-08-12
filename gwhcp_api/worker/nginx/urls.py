from django.urls import path

from worker.nginx import views

app_name = 'nginx'

urlpatterns = [
    path(
        'create/indexes/config',
        views.CreateIndexesConfig.as_view(),
        name='create-indexes-config'
    ),

    path(
        'create/logs/config',
        views.CreateLogsConfig.as_view(),
        name='create-logs-config'
    ),

    path(
        'create/python3/config',
        views.CreatePython3Config.as_view(),
        name='create-python3-config'
    ),

    path(
        'create/virtual/config',
        views.CreateVirtualConfig.as_view(),
        name='create-virtual-config'
    ),

    path(
        'delete/indexes/config',
        views.DeleteIndexesConfig.as_view(),
        name='delete-indexes-config'
    ),

    path(
        'delete/logs/config',
        views.DeleteLogsConfig.as_view(),
        name='delete-logs-config'
    ),

    path(
        'delete/python3/config',
        views.DeletePython3Config.as_view(),
        name='delete-python3-config'
    ),

    path(
        'delete/virtual/config',
        views.DeleteVirtualConfig.as_view(),
        name='delete-virtual-config'
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

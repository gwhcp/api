from django.urls import path

from worker.php import views

app_name = 'php'

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

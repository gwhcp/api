from django.urls import path

from worker.dovecot import views

app_name = 'dovecot'

urlpatterns = [
    path(
        'create/config/ssl',
        views.CreateConfigSsl.as_view(),
        name='create-ssl-config'
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

from django.urls import path

from worker.rabbitmq import views

app_name = 'rabbitmq'

urlpatterns = [
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

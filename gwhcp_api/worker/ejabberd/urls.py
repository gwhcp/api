from django.urls import path

from worker.ejabberd import views

app_name = 'ejabberd'

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

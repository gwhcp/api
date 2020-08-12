from django.urls import path

from worker.daemon import views

app_name = 'daemon'

urlpatterns = [
    path(
        'celery/install',
        views.CeleryInstall.as_view(),
        name='celery-install'
    ),

    path(
        'celery/uninstall',
        views.CeleryUninstall.as_view(),
        name='celery-uninstall'
    ),

    path(
        'ipaddress/install',
        views.IpaddressInstall.as_view(),
        name='ipaddress-install'
    ),

    path(
        'ipaddress/uninstall',
        views.IpaddressUninstall.as_view(),
        name='ipaddress-uninstall'
    ),

    path(
        'worker/install',
        views.WorkerInstall.as_view(),
        name='worker-install'
    ),

    path(
        'worker/uninstall',
        views.WorkerUninstall.as_view(),
        name='worker-uninstall'
    )
]

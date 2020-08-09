from django.urls import path

from worker.web import views

app_name = 'web'

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
        'ssl/install',
        views.SslInstall.as_view(),
        name='ssl-install'
    ),

    path(
        'ssl/uninstall',
        views.SslUninstall.as_view(),
        name='ssl-uninstall'
    )
]

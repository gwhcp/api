from django.urls import path

from worker.cron import views

app_name = 'cron'

urlpatterns = [
    path(
        'create/config',
        views.CreateConfig.as_view(),
        name='create-config'
    ),

    path(
        'create/domain',
        views.CreateDomain.as_view(),
        name='create-domain'
    ),

    path(
        'delete/config',
        views.DeleteConfig.as_view(),
        name='delete-config'
    ),

    path(
        'delete/domain',
        views.DeleteDomain.as_view(),
        name='delete-domain'
    )
]

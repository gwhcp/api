from django.urls import path

from worker.gunicorn import views

app_name = 'gunicorn'

urlpatterns = [
    path(
        'create/config',
        views.CreateConfig.as_view(),
        name='create-config'
    ),

    path(
        'create/service',
        views.CreateService.as_view(),
        name='create-service'
    ),

    path(
        'delete/config',
        views.DeleteConfig.as_view(),
        name='delete-config'
    ),

    path(
        'delete/service',
        views.DeleteService.as_view(),
        name='delete-service'
    )
]

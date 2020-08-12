from django.urls import path

from worker.awstats import views

app_name = 'awstats'

urlpatterns = [
    path(
        'create/auth',
        views.CreateAuth.as_view(),
        name='create-auth'
    ),

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
        'update/all',
        views.UpdateAll.as_view(),
        name='update-all'
    ),

    path(
        'update/domain',
        views.UpdateDomain.as_view(),
        name='update-domain'
    )
]

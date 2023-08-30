from django.urls import path

from admin.network.queue import views

urlpatterns = [
    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        'retry',
        views.Retry.as_view(),
        name='retry'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

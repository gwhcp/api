from django.urls import path

from admin.network.queue import views

urlpatterns = [
    path(
        'profile/<int:pk>',
        views.Profile.as_view(),
        name='profile'
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

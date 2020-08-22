from django.urls import path

from hardware.client import views

urlpatterns = [
    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        'delete/<int:pk>',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        'install/<int:pk>',
        views.Install.as_view(),
        name='install'
    ),

    path(
        'profile/<int:pk>',
        views.Profile.as_view(),
        name='profile'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

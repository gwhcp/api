from django.urls import path

from billing.payment import views

urlpatterns = [
    path(
        'authorize/<int:pk>/authentication',
        views.AuthorizeAuthentication.as_view(),
        name='authorize-authentication'
    ),

    path(
        'authorize/<int:pk>/method',
        views.AuthorizeMethod.as_view(),
        name='authorize-method'
    ),

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

from django.urls import path

from admin.customer.account import views

urlpatterns = [
    path(
        'accesslog/<int:pk>',
        views.AccessLog.as_view(),
        name='accesslog'
    ),

    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

    path(
        'password',
        views.Password.as_view(),
        name='password'
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

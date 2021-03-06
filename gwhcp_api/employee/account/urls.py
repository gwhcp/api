from django.urls import path

from employee.account import views

urlpatterns = [
    path(
        'accesslog',
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
        'profile',
        views.Profile.as_view(),
        name='profile'
    )
]

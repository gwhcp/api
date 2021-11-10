from django.urls import path

from admin.employee.mail import views

urlpatterns = [
    path(
        'password/<int:pk>',
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

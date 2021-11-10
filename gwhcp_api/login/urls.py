from django.urls import path

from login import views

urlpatterns = [
    path(
        'permissions',
        views.Permissions.as_view(),
        name='permissions'
    ),

    path(
        'profile',
        views.Profile.as_view(),
        name='profile'
    )
]

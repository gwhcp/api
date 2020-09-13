from django.urls import path

from employee.xmpp import views

urlpatterns = [
    path(
        'profile',
        views.Profile.as_view(),
        name='profile'
    )
]

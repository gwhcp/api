from django.urls import path

from admin.employee.xmpp import views

urlpatterns = [
    path(
        'profile',
        views.Profile.as_view(),
        name='profile'
    )
]

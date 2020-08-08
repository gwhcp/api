from django.urls import path

from hardware.client import views

urlpatterns = [
    path(
        'choice/domain',
        views.ChoiceDomain.as_view(),
        name='choice-domain'
    ),

    path(
        'choice/hardware',
        views.ChoiceHardware.as_view(),
        name='choice-hardware'
    ),

    path(
        'choice/target',
        views.ChoiceTarget.as_view(),
        name='choice-target'
    ),

    path(
        'choice/web',
        views.ChoiceWeb.as_view(),
        name='choice-web'
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

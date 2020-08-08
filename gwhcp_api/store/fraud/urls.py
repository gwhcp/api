from django.urls import path

from store.fraud import views

urlpatterns = [
    path(
        'choice/type',
        views.ChoiceType.as_view(),
        name='choice-type'
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

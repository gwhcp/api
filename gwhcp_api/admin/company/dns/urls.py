from django.urls import path

from admin.company.dns import views

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
        'delete/<int:domain>/<int:pk>',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        'ns/<int:domain>',
        views.Ns.as_view(),
        name='ns'
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
    ),

    path(
        'search/<int:pk>',
        views.SearchRecord.as_view(),
        name='search-record'
    )
]

from django.urls import path

from admin.company.xmpp import views

urlpatterns = [
    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

    path(
        'create',
        views.CreateAccount.as_view(),
        name='create'
    ),

    path(
        'create/group',
        views.CreateGroup.as_view(),
        name='create-group'
    ),

    path(
        'delete/<int:pk>',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        'delete/group/<int:pk>',
        views.DeleteGroup.as_view(),
        name='delete-group'
    ),

    path(
        'profile/<int:pk>',
        views.Profile.as_view(),
        name='profile'
    ),

    path(
        'rebuild',
        views.Rebuild.as_view(),
        name='rebuild'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    ),

    path(
        'search/group',
        views.SearchGroup.as_view(),
        name='search-group'
    )
]

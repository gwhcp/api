from django.urls import path

from client.billing import views

urlpatterns = [
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
        'profile/invoice/<int:profile_id>/<int:pk>',
        views.ProfileInvoice.as_view(),
        name='profile-invoice'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    ),

    path(
        'search/invoice/<int:pk>',
        views.SearchInvoice.as_view(),
        name='search-invoice'
    )
]

from django.urls import path

from client.billing import views

urlpatterns = [
    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

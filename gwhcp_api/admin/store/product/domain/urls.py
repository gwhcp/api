from django.urls import path

from admin.store.product.domain import views

urlpatterns = [
    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        '<int:pk>/delete',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        '<int:pk>/resource',
        views.Resource.as_view(),
        name='resource'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

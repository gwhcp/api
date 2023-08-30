from django.urls import path

from admin.store.product.price import views

urlpatterns = [
    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        '<int:pk>/delete/<int:store_product_id>',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        '<int:pk>/edit/<int:store_product_id>',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        '<int:store_product_id>/search',
        views.Search.as_view(),
        name='search'
    )
]

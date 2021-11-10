from django.urls import path

from admin.store.product.price import views

urlpatterns = [
    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        'delete/<int:store_product_id>/<int:pk>',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        'profile/<int:store_product_id>/<int:pk>',
        views.Profile.as_view(),
        name='profile'
    ),

    path(
        'search/<int:store_product_id>',
        views.Search.as_view(),
        name='search'
    )
]

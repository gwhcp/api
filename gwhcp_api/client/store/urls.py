from django.urls import path

from client.store import views

urlpatterns = [
    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        'search/prices/<int:pk>',
        views.SearchPrices.as_view(),
        name='search-prices'
    ),

    path(
        'search/product/domain',
        views.SearchProductDomain.as_view(),
        name='search-product-domain'
    ),

    path(
        'search/types',
        views.SearchProductTypes.as_view(),
        name='search-types'
    )
]

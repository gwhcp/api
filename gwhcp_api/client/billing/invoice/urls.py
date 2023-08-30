from django.urls import path

from client.billing.invoice import views

urlpatterns = [
    path(
        '<int:profile_id>/invoice/<int:pk>',
        views.Invoice.as_view(),
        name='invoice'
    ),

    path(
        '<int:profile_id>/search',
        views.Search.as_view(),
        name='search'
    )
]

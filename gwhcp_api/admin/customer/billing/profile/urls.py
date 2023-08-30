from django.urls import path

from admin.customer.billing.profile import views

urlpatterns = [
    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

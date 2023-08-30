from django.urls import path

from admin.customer.order import views

urlpatterns = [
    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

    path(
        '<int:pk>/fraud',
        views.Fraud.as_view(),
        name='fraud'
    ),

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

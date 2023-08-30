from django.urls import path

from admin.customer.account import views

urlpatterns = [
    path(
        '<int:pk>/accesslog',
        views.AccessLog.as_view(),
        name='accesslog'
    ),

    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

    path(
        '<int:pk>/edit',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        '<int:pk>/password',
        views.Password.as_view(),
        name='password'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

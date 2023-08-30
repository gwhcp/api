from django.urls import path

from admin.hardware.client import views

urlpatterns = [
    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

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
        '<int:pk>/install',
        views.Install.as_view(),
        name='install'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    )
]

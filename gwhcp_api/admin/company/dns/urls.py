from django.urls import path

from admin.company.dns import views

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
        '<int:domain>/ns',
        views.Ns.as_view(),
        name='ns'
    ),

    path(
        '<int:pk>/search',
        views.Search.as_view(),
        name='search'
    )
]

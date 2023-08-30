from django.urls import path

from admin.company.mail import views

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
        '<int:pk>/edit/<int:domain_id>',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        '<int:pk>/password',
        views.Password.as_view(),
        name='password'
    ),

    path(
        '<int:pk>/search',
        views.Search.as_view(),
        name='search'
    )
]

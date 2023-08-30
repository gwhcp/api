from django.urls import path

from admin.employee.mail import views

urlpatterns = [
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

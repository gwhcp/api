from django.urls import path

from admin.employee.account import views

urlpatterns = [
    path(
        'accesslog',
        views.AccessLog.as_view(),
        name='accesslog'
    ),

    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    ),

    path(
        'edit',
        views.Edit.as_view(),
        name='edit'
    ),

    path(
        'password',
        views.Password.as_view(),
        name='password'
    )
]

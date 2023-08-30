from django.urls import path

from admin.company.account import views

urlpatterns = [
    path(
        'edit',
        views.Edit.as_view(),
        name='edit'
    )
]

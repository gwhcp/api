from django.urls import path

from admin.store.product import views

urlpatterns = [
    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    )
]

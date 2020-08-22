from django.urls import path

from store.product import views

urlpatterns = [
    path(
        'choices',
        views.Choices.as_view(),
        name='choices'
    )
]

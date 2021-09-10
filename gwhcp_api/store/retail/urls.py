from django.urls import path

from store.retail import views

urlpatterns = [
    path(
        'create',
        views.Create.as_view(),
        name='create'
    )
]

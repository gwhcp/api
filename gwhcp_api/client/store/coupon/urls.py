from django.urls import path

from client.store.coupon import views

urlpatterns = [
    path(
        'validate/<str:name>',
        views.Validate.as_view(),
        name='validate'
    )
]

from django.urls import path

from worker.console import views

app_name = 'console'

urlpatterns = [
    path(
        'ders',
        views.DERS.as_view(),
        name='ders'
    )
]

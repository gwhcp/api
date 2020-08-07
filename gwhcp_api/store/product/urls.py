from django.urls import path

from store.product import views

urlpatterns = [
    path('choice/company', views.ChoiceCompany.as_view(), name='choice-company'),
    path('choice/ip', views.ChoiceIpType.as_view(), name='choice-ip'),
    path('choice/web', views.ChoiceWeb.as_view(), name='choice-web')
]

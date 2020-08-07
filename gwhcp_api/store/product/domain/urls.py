from django.urls import path

from store.product.domain import views

urlpatterns = [
    path('create', views.Create.as_view(), name='create'),
    path('delete/<int:pk>', views.Delete.as_view(), name='delete'),
    path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
    path('resource/<int:pk>', views.Resource.as_view(), name='resource'),
    path('search', views.Search.as_view(), name='search')
]

from django.urls import path

from setting.banned import views

urlpatterns = [
    path('choice/type', views.ChoiceTypes.as_view(), name='choice-types'),
    path('create', views.Create.as_view(), name='create'),
    path('delete/<int:pk>', views.Delete.as_view(), name='delete'),
    path('profile/<int:pk>', views.Profile.as_view(), name='profile'),
    path('search', views.Search.as_view(), name='search')
]

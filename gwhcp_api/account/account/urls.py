from django.urls import path

from account.account import views

urlpatterns = [
    path('accesslog', views.AccessLog.as_view(), name='accesslog'),
    path('accesslog/<int:pk>', views.ManageAccessLog.as_view(), name='manage-accesslog'),
    path('choice/commentorder', views.ChoiceCommentOrder.as_view(), name='choice-comment-order'),
    path('choice/timeformat', views.ChoiceTimeFormat.as_view(), name='choice-time-format'),
    path('choice/timezone', views.ChoiceTimeZone.as_view(), name='choice-time-zone'),
    path('profile', views.Profile.as_view(), name='profile'),
    path('profile/<int:pk>', views.ManageProfile.as_view(), name='manage-profile'),
    path('search', views.Search.as_view(), name='search')
]

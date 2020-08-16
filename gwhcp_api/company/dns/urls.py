from django.urls import path

from company.dns import views

urlpatterns = [
    path(
        'choice/ns',
        views.ChoiceNs.as_view(),
        name='choice-ns'
    ),

    path(
        'choice/recordtype',
        views.ChoiceRecordType.as_view(),
        name='choice-record-type'
    ),

    path(
        'create',
        views.Create.as_view(),
        name='create'
    ),

    path(
        'delete/<int:domain>/<int:pk>',
        views.Delete.as_view(),
        name='delete'
    ),

    path(
        'ns/<int:domain>',
        views.Ns.as_view(),
        name='ns'
    ),

    path(
        'profile/<int:pk>',
        views.Profile.as_view(),
        name='profile'
    ),

    path(
        'search',
        views.Search.as_view(),
        name='search'
    ),

    path(
        'search/<int:pk>',
        views.SearchRecord.as_view(),
        name='search-record'
    )
]

from django.urls import path

from worker.mail import views

app_name = 'mail'

urlpatterns = [
    path(
        'create/domain',
        views.CreateDomain.as_view(),
        name='create-domain'
    ),

    path(
        'create/forward',
        views.CreateForward.as_view(),
        name='create-forward'
    ),

    path(
        'create/list',
        views.CreateList.as_view(),
        name='create-list'
    ),

    path(
        'create/mailbox',
        views.CreateMailbox.as_view(),
        name='create-mailbox'
    ),

    path(
        'delete/domain',
        views.DeleteDomain.as_view(),
        name='delete-domain'
    ),

    path(
        'delete/forward',
        views.DeleteForward.as_view(),
        name='delete-forward'
    ),

    path(
        'delete/list',
        views.DeleteList.as_view(),
        name='delete-list'
    ),

    path(
        'delete/mailbox',
        views.DeleteMailbox.as_view(),
        name='delete-mailbox'
    ),

    path(
        'disable',
        views.Disable.as_view(),
        name='disable'
    ),

    path(
        'enable',
        views.Enable.as_view(),
        name='enable'
    ),

    path(
        'update/forward',
        views.UpdateForward.as_view(),
        name='update-forward'
    ),

    path(
        'update/mailbox',
        views.UpdateMailbox.as_view(),
        name='update-mailbox'
    )
]

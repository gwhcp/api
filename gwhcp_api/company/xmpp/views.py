from django.db import connections
from rest_framework import generics
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from company.xmpp import models
from company.xmpp import serializers
from login import gacl
from utils import security


class Choices(views.APIView):
    """
    Choices
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        result = {
            'account': {},
            'group': {}
        }

        # Account
        for account in models.Account.objects.all():
            result['account'].update({
                account.pk: account.get_full_name()
            })

        # Group
        for group in models.ProsodyGroup.objects.all():
            result['group'].update({
                group.pk: group.name
            })

        return Response(result)


class CreateAccount(generics.CreateAPIView):
    """
    Create company xmpp account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount'],
        'add': ['company.xmpp.add_prosodyaccount']
    }

    queryset = models.ProsodyAccount.objects.all()

    serializer_class = serializers.CreateAccountSerializer


class CreateGroup(generics.CreateAPIView):
    """
    Create company xmpp group
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount'],
        'add': ['company.xmpp.add_prosodyaccount']
    }

    queryset = models.ProsodyGroup.objects.all()

    serializer_class = serializers.CreateGroupSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company xmpp account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount'],
        'delete': ['company.xmpp.delete_prosodyaccount']
    }

    queryset = models.ProsodyAccount.objects.all()

    serializer_class = serializers.SearchSerializer


class DeleteGroup(generics.RetrieveDestroyAPIView):
    """
    Delete company xmpp group
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount'],
        'delete': ['company.xmpp.delete_prosodyaccount']
    }

    queryset = models.ProsodyGroup.objects.all()

    serializer_class = serializers.SearchGroupSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        account = models.ProsodyAccount.objects.filter(
            group=kwargs['pk']
        )

        if account.exists():
            return Response(
                {
                    'non_form_field_error': 'Group is currently in use.'
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED
            )

        self.perform_destroy(instance)

        return Response(status=status.HTTP_204_NO_CONTENT)


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit company xmpp account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount'],
        'change': ['company.xmpp.change_prosodyaccount']
    }

    queryset = models.ProsodyAccount.objects.all()

    serializer_class = serializers.ProfileSerializer


class Rebuild(generics.ListAPIView):
    """
    Rebuild XMPP Roster
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount']
    }

    queryset = models.ProsodyAccount.objects.all()

    serializer_class = serializers.RebuildSerializer

    def get(self, request, *args, **kwargs):
        cursor = connections['xmpp'].cursor()
        cursor.execute('TRUNCATE TABLE ' + models.Prosody._meta.db_table + ' RESTART IDENTITY CASCADE')
        cursor.execute('TRUNCATE TABLE ' + models.ProsodyArchive._meta.db_table + ' RESTART IDENTITY CASCADE')

        result = models.ProsodyAccount.objects.all()

        for user in result:
            password = security.xmpp_password(
                security.decrypt_string(user.password)
            )

            models.Prosody.objects.bulk_create([
                models.Prosody(
                    host='localhost',
                    user=user.account_id,
                    store='accounts',
                    key='iteration_count',
                    type='number',
                    value=4096
                ),
                models.Prosody(
                    host='localhost',
                    user=user.account_id,
                    store='accounts',
                    key='salt',
                    type='string',
                    value=password['salt']
                ),
                models.Prosody(
                    host='localhost',
                    user=user.account_id,
                    store='accounts',
                    key='server_key',
                    type='string',
                    value=password['server_key']
                ),
                models.Prosody(
                    host='localhost',
                    user=user.account_id,
                    store='accounts',
                    key='stored_key',
                    type='string',
                    value=password['stored_key']
                ),
                models.Prosody(
                    host='localhost',
                    user=user.account_id,
                    store='roster',
                    key=None,
                    type='json',
                    value='{"__hash":[false,{"pending":{},"version":8}]}'
                ),
                models.Prosody(
                    host='localhost',
                    user=user.account_id,
                    store='pep',
                    key='http://jabber.org/protocol/tune',
                    type='json',
                    value='{"subscribers":{},"name":"http://jabber.org/protocol/tune","config":{},"affiliations":{}}'
                )
            ])

            for other in result:
                if user.account_id != other.account_id:
                    employee = models.Account.objects.get(pk=other.account_id)

                    models.Prosody.objects.create(
                        host='localhost',
                        user=user.account_id,
                        store='roster',
                        key=f"{other.account_id}@localhost",
                        type='json',
                        value=f'{{"name":"{employee.get_full_name()}","subscription":"both","groups":{{"Buddies":true}}}}'
                    )

        return Response(
            {
                'response': 'XMPP User and Groups have been rebuilt.'
            }
        )


class Search(generics.ListAPIView):
    """
    Search company xmpp accounts
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount']
    }

    queryset = models.ProsodyAccount.objects.all()

    serializer_class = serializers.SearchSerializer


class SearchGroup(generics.ListAPIView):
    """
    Search company xmpp groups
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company.xmpp.view_prosodyaccount']
    }

    queryset = models.ProsodyGroup.objects.all()

    serializer_class = serializers.SearchGroupSerializer

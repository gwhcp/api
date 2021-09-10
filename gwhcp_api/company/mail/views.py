from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from company.mail import models
from company.mail import serializers
from login import gacl
from utils import security
from worker.queue.create import CreateQueue


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
            'company': {},
            'domain': {},
            'type': {}
        }

        # Account
        for account in models.Account.objects.all():
            result['account'].update({
                account.pk: account.get_full_name()
            })

        # Company
        for company in models.Company.objects.all():
            result['company'].update({
                company.pk: company.name
            })

        # Domain
        for domain in models.Domain.objects.all():
            result['domain'].update({
                domain.pk: domain.name
            })

        # Mail Type
        result['type'].update(dict(models.Mail.Type.choices))

        return Response(result)


class Create(generics.CreateAPIView):
    """
    Create company mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_mail.view_mail'],
        'add': ['company_mail.add_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.CreateSerializer

    def perform_create(self, serializer):
        instance = serializer.save()

        server = models.Server.objects.get(allowed=instance.domain)

        create_queue = CreateQueue(
            service_id={
                'mail_id': instance.pk
            }
        )

        # Forward
        if instance.mail_type == 'forward':
            create_queue.item(
                {
                    'ipaddress': server.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.create_forward',
                    'args': {
                        'domain': instance.domain.name,
                        'email': instance.forward_to,
                        'user': instance.name
                    }
                }
            )

        # Mailbox
        if instance.mail_type == 'mailbox':
            create_queue.item(
                {
                    'ipaddress': server.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.create_mailbox',
                    'args': {
                        'domain': instance.domain.name,
                        'password': security.decrypt_string(instance.password),
                        'user': instance.name,
                        'quota': instance.quota
                    }
                }
            )


class Delete(generics.RetrieveDestroyAPIView):
    """
    Delete company mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_mail.view_mail'],
        'delete': ['company_mail.delete_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        server = models.Server.objects.get(allowed=instance.domain)

        create_queue = CreateQueue()

        # Forward
        if instance.mail_type == 'forward':
            create_queue.item(
                {
                    'ipaddress': server.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.delete_forward',
                    'args': {
                        'domain': instance.domain.name,
                        'user': instance.name
                    }
                }
            )

        # Mailbox
        if instance.mail_type == 'mailbox':
            create_queue.item(
                {
                    'ipaddress': server.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.delete_mailbox',
                    'args': {
                        'domain': instance.domain.name,
                        'user': instance.name
                    }
                }
            )

        instance.delete()


class Password(generics.RetrieveUpdateAPIView):
    """
    View and edit company mail account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_mail.view_mail'],
        'change': ['company_mail.change_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.PasswordSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        # Mailbox
        if instance.mail_type == 'mailbox':
            server = models.Server.objects.get(allowed=instance.domain)

            create_queue = CreateQueue(
                service_id={
                    'mail_id': instance.pk
                }
            )

            create_queue.item(
                {
                    'ipaddress': server.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.update_mailbox',
                    'args': {
                        'domain': instance.domain.name,
                        'password': security.decrypt_string(instance.password),
                        'user': instance.name,
                        'quota': instance.quota
                    }
                }
            )


class Profile(generics.RetrieveUpdateAPIView):
    """
    View and edit company mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_mail.view_mail'],
        'change': ['company_mail.change_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.ProfileSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        server = models.Server.objects.get(allowed=instance.domain)

        create_queue = CreateQueue(
            service_id={
                'mail_id': instance.pk
            }
        )

        # Forward
        if instance.mail_type == 'forward':
            create_queue.item(
                {
                    'ipaddress': server.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.update_forward',
                    'args': {
                        'domain': instance.domain.name,
                        'email': instance.forward_to,
                        'user': instance.name
                    }
                }
            )

        # Mailbox
        if instance.mail_type == 'mailbox':
            create_queue.item(
                {
                    'ipaddress': server.ipaddress_pool.ipaddress,
                    'name': 'mail.tasks.update_mailbox',
                    'args': {
                        'domain': instance.domain.name,
                        'password': security.decrypt_string(instance.password),
                        'user': instance.name,
                        'quota': instance.quota
                    }
                }
            )


class Search(generics.ListAPIView):
    """
    Search company mail accounts
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['company_mail.view_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.SearchSerializer

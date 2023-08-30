from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.company.mail import models
from admin.company.mail import serializers
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
        """
        View for retrieving choices for account, domain, and mail type.

        Parameters:
        - request: The request object.

        Return Type:
        - Response
        """

        result = {
            'account': {},
            'domain': {},
            'type': {}
        }

        # Account
        for account in models.Account.objects.all():
            result['account'].update({
                account.pk: account.get_full_name()
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
        'view': ['admin_company_mail.view_mail'],
        'add': ['admin_company_mail.add_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.CreateSerializer

    def perform_create(self, serializer):
        """
        Method Name: perform_create

        Parameters:
        - serializer (Serializer): The serializer used to save the instance.

        Return Type: None

        Description:
        This method is used to perform additional actions after saving an instance using the provided serializer. It retrieves the saved instance, finds the corresponding server, and creates a task in the create queue based on the type of mail.
        """

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
        'view': ['admin_company_mail.view_mail'],
        'delete': ['admin_company_mail.delete_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        Performs the deletion of a mail instance.

        Parameters:
        - instance: The mail instance to be deleted.

        Returns:
        None
        """

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


class Edit(generics.RetrieveUpdateAPIView):
    """
    View and edit company mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_mail.view_mail'],
        'change': ['admin_company_mail.change_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.ProfileSerializer

    def perform_update(self, serializer):
        """
        Method: perform_update

        Parameters:
        - serializer: The serializer object used to validate and save the updated instance.

        Return:
        - None

        Description:
        This method is used to perform the update operation after the serializer saves the instance.
        It retrieves the saved instance and obtains the server associated with the instance's domain.
        Then, it creates a CreateQueue object with the service_id attribute set to the mail_id of the instance.
        Based on the mail_type of the instance, it adds a task to the create_queue.

        If the mail_type is 'forward', it adds a task to update the forward settings using the `update_forward` task.
        The task includes the IP address of the server, the domain name, the email address to forward to, and the user.

        If the mail_type is 'mailbox', it adds a task to update the mailbox settings using the `update_mailbox` task.
        The task includes the IP address of the server, the domain name, the decrypted password, the user, and the quota.
        """

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


class Password(generics.RetrieveUpdateAPIView):
    """
    View and edit company mail account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_mail.view_mail'],
        'change': ['admin_company_mail.change_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.PasswordSerializer

    def perform_update(self, serializer):
        """
        This method is responsible for performing the update operation on the serializer instance.

        Parameters:
        - serializer: An instance of the serializer class used for updating the data.

        Returns:
        None
        """

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


class Search(generics.ListAPIView):
    """
    Search company mail accounts
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_company_mail.view_mail']
    }

    queryset = models.Mail.objects.all()

    serializer_class = serializers.SearchSerializer

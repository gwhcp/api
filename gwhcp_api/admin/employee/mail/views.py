from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from admin.employee.mail import models
from admin.employee.mail import serializers
from login import gacl
from utils import security
from worker.queue.create import CreateQueue


class Edit(generics.RetrieveAPIView):
    """
    View employee mail account
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_employee_mail.view_mail']
    }

    serializer_class = serializers.ProfileSerializer

    def get_object(self):
        return models.Mail.objects.get(
            pk=self.kwargs['pk'],
            account_id=self.request.user.pk
        )


class Password(generics.RetrieveUpdateAPIView):
    """
    View and edit employee mail account password
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_employee_mail.view_mail'],
        'change': ['admin_employee_mail.change_mail']
    }

    serializer_class = serializers.PasswordSerializer

    def get_object(self):
        return models.Mail.objects.get(
            pk=self.kwargs['pk'],
            account_id=self.request.user.pk
        )

    def perform_update(self, serializer):
        """
        Method: perform_update

        This method is used to perform an update operation for a given serializer instance. It takes a serializer as a parameter and does not return any value.

        Parameters:
        - serializer: An instance of a serializer class.
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
    Search employee mail accounts
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_employee_mail.view_mail']
    }

    serializer_class = serializers.SearchSerializer

    def get_queryset(self):
        return models.Mail.objects.filter(
            account_id=self.request.user.pk
        )

from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.store.product import models


class Choices(views.APIView):
    """
    This class provides an API endpoint for retrieving choices for IP address types.

    Attributes:
        - permission_classes (tuple): A tuple containing the permission classes for this view. Only admin users are allowed.

    Methods:
        - get(request): Retrieves the available choices for IP address types.
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        """
        Endpoint for retrieving choices for IP address types.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: The HTTP response object containing the available choices for IP address types.
        """
        result = {
            'ip_type': {}
        }

        # IP Address Type
        result['ip_type'].update(dict(models.StoreProduct.IpaddressType.choices))

        return Response(result)

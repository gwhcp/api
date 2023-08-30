from rest_framework import exceptions
from rest_framework import generics
from rest_framework import views
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from admin.store.fraud import models
from admin.store.fraud import serializers
from login import gacl


class Choices(views.APIView):
    """
    Class: Choices

    A class that represents an API view for retrieving a dictionary of choices.

    Attributes:
    - permission_classes (tuple): A tuple of permission classes for this API view.

    Methods:
    - get(request):
        This method retrieves a dictionary of choices.

        Parameters:
        - request (Request): The request object.

        Return type:
        - Response: The response containing the dictionary of choices.
    """

    permission_classes = (
        IsAdminUser,
    )

    def get(self, request):
        """
        This is a documentation for the `get` method.

        Parameters:
        - request: The request object.

        Return type:
        - Response: The response containing the dictionary of choices.
        """

        return Response(dict(models.FraudString.Type.choices))


class Create(generics.CreateAPIView):
    """
    The `Create` class is a subclass of `generics.CreateAPIView` provided by the Django Rest Framework.
    It is used for creating instances of the `FraudString` model in the database.

    Attributes:
        - permission_classes (tuple): Specifies the permission classes required to access this view.
        - gacl (dict): Contains the permissions required for this view based on the `gacl` module.
        - queryset (QuerySet): Specifies the queryset for retrieving instances of the `FraudString` model.
        - serializer_class (Serializer): Specifies the serializer class used for validating and serializing data.

    Note: This class requires the `gacl` module and the `rest_framework` library to be imported in order to work properly.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_fraud.view_fraudstring'],
        'add': ['admin_store_fraud.add_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.CreateSerializer


class Delete(generics.RetrieveDestroyAPIView):
    """
    The `Delete` class is a generic view that inherits from `RetrieveDestroyAPIView` provided by the `generics` module in the Django Rest Framework. It is used for deleting instances of the `FraudString` model.

    Attributes:
        - `permission_classes`: A tuple of permission classes required to access this view. It includes the `GaclPermissions` class from the `gacl` module and the `IsAdminUser` class from the Django Rest Framework.
        - `gacl`: A dictionary specifying the required permissions for different CRUD operations on the `FraudString` model.
        - `queryset`: A queryset that retrieves all `FraudString` instances.
        - `serializer_class`: The serializer class used for validating and deserializing the incoming request data.

    Methods:
        - `perform_destroy(instance)`: Deletes the `instance` if it's not currently in use. If the `FraudString` instance is currently in use and cannot be removed, a `ValidationError` is raised.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_fraud.view_fraudstring'],
        'delete': ['admin_store_fraud.delete_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.SearchSerializer

    def perform_destroy(self, instance):
        """
        Deletes the instance if it's not currently in use.

        Parameters:
            instance (Object): Instance of the fraud string.

        Raises:
            ValidationError: If the fraud string is currently in use and cannot be removed.
        """

        if not instance.can_delete():
            raise exceptions.ValidationError(
                'Fraud string is currently in use and cannot be removed.',
                code='can_delete'
            )

        instance.delete()


class Edit(generics.RetrieveUpdateAPIView):
    """
    Edit

    Class for editing a FraudString object.

    Attributes:
        permission_classes (tuple): Tuple of permission classes required for accessing this view.
        gacl (dict): Dictionary defining the gacl permissions required for each action.
        queryset (QuerySet): QuerySet of FraudString objects.
        serializer_class (Serializer): Serializer class for handling the serialization and deserialization of data.

    Methods:
        get_queryset(): Returns the queryset to be used for retrieving the FraudString object.
        get_serializer(): Returns the serializer instance to be used for handling serialization and deserialization.
        retrieve(): Retrieves and returns a FraudString object.
        update(): Updates an existing FraudString object and returns the updated object.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'change': ['admin_store_fraud.change_fraudstring'],
        'view': ['admin_store_fraud.view_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.ProfileSerializer


class Search(generics.ListAPIView):
    """
    Search

    This class is a generic list view for searching FraudString objects in the admin store fraud module.

    Attributes:
    - permission_classes (tuple): A tuple containing the permission classes required to access this view.
    - gacl (dict): A dictionary representing the permissions required for each view action.
    - queryset (QuerySet): The queryset of FraudString objects that will be searched.
    - serializer_class (Serializer): The serializer class used to serialize the search results.
    """

    permission_classes = (
        gacl.GaclPermissions,
        IsAdminUser
    )

    gacl = {
        'view': ['admin_store_fraud.view_fraudstring']
    }

    queryset = models.FraudString.objects.all()

    serializer_class = serializers.SearchSerializer

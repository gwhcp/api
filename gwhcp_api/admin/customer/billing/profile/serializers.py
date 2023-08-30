import datetime

from rest_framework import serializers

from admin.customer.billing.profile import models
from utils.merchant import cim


class ProfileSerializer(serializers.ModelSerializer):
    address = serializers.RegexField(
        allow_null=False,
        max_length=255,
        regex='^[a-zA-Z0-9 #.\'-]+$',
        required=True
    )

    city = serializers.RegexField(
        allow_null=False,
        max_length=255,
        regex='^[a-zA-Z .\'-]+$',
        required=True
    )

    country = serializers.RegexField(
        allow_null=False,
        max_length=2,
        regex='^[a-zA-Z]+$',
        required=True
    )

    credit_card_cvv2 = serializers.RegexField(
        allow_null=False,
        min_length=3,
        max_length=4,
        regex='^[0-9]+$',
        required=True
    )

    credit_card_month = serializers.RegexField(
        allow_null=False,
        min_length=2,
        max_length=2,
        regex='^[0-9]+$',
        required=True
    )

    credit_card_name = serializers.CharField(
        read_only=True
    )

    credit_card_number = serializers.CharField(
        read_only=True
    )

    credit_card_type = serializers.CharField(
        read_only=True
    )

    credit_card_year = serializers.RegexField(
        allow_null=False,
        min_length=4,
        max_length=4,
        regex='^[0-9]+$',
        required=True
    )

    primary_phone = serializers.RegexField(
        allow_null=False,
        max_length=30,
        regex='^[0-9]+$',
        required=True
    )

    state = serializers.RegexField(
        allow_null=False,
        max_length=3,
        regex='^[a-zA-Z]+$',
        required=True
    )

    zipcode = serializers.CharField(
        allow_null=False,
        max_length=28,
        required=True
    )

    class Meta:
        model = models.BillingProfile

        fields = '__all__'

        read_only_fields = (
            'account',
            'authorize_payment_id',
            'authorize_profile_id',
            'payment_gateway'
        )

    def update(self, instance, validated_data):
        """
        Update method for ProfileSerializer class.

        This method is used to update an existing instance of the Profile model.

        Parameters:
        - instance (Profile): The instance of the Profile model to be updated.
        - validated_data (dict): The validated data containing the updated fields.

        Returns:
        - validated_data (dict): The updated validated data.

        Raises:
        - serializers.ValidationError: If there is an error during the update process.
        """

        validated_data.update({
            'credit_card_name': instance.credit_card_name,
            'credit_card_number': instance.credit_card_number
        })

        result = cim.PaymentGateway(validated_data, instance).update_cim()

        if result['error']:
            raise serializers.ValidationError(
                {
                    'non_field_errors': result['message']
                },
                code='error'
            )

        return validated_data

    def validate(self, attrs):
        """
        Validates the profile attributes.

        :param attrs: A dictionary containing the profile attributes.

        :raises ValidationError: If the credit card has expired.

        :returns: A dictionary containing the validated profile attributes.
        """

        if datetime.date(int(attrs['credit_card_year']), int(attrs['credit_card_month']), 1) < datetime.date.today():
            raise serializers.ValidationError(
                {
                    'credit_card_number': 'Credit card has expired.'
                },
                code='expired'
            )

        return attrs

    def validate_credit_card_cvv2(self, value):
        """
        Validate a credit card CVV.

        Args:
            value (int): The CVV to validate.

        Returns:
            int: The validated CVV.

        Raises:
            serializers.ValidationError: If the CVV is not between 3 and 4 characters long.
        """

        if len(str(value)) < 3 or len(str(value)) > 4:
            raise serializers.ValidationError(
                'Credit Card CVV must be between 3 and 4 characters long',
                code='invalid'
            )

        return value

    def validate_credit_card_month(self, value):
        """
        Validates the credit card expiration month.

        Method Name: validate_credit_card_month

        Parameters:
        - value (str): The value representing the credit card expiration month.

        Return Type:
        - str: The validated credit card expiration month.

        Description:
        This method validates the given credit card expiration month. It checks if the month is a valid two-digit value between '01' and '12'. If the month is not valid, it raises a validation error with a message indicating that the expiration month is not valid. If the month is valid, it returns the same value.
        """

        months = [
            '01',
            '02',
            '03',
            '04',
            '05',
            '06',
            '07',
            '08',
            '09',
            '10',
            '11',
            '12'
        ]

        if str(value) not in months:
            raise serializers.ValidationError(
                'Expiration month is not valid.',
                code='invalid'
            )

        return value

    def validate_credit_card_year(self, value):
        """
        Validates the credit card expiration year.

        Parameters:
        - value (int): The credit card expiration year.

        Raises:
        - serializers.ValidationError: If the credit card has expired.

        Returns:
        - int: The validated credit card expiration year.
        """

        if str(value) < str(datetime.date.today().year):
            raise serializers.ValidationError(
                'Credit card has expired.',
                code='invalid'
            )

        return value

    def validate_name(self, value):
        """
        Method: validate_name

        Description: This method is used to validate the name field of a profile. It checks if the name already exists in the BillingProfile model, excluding the current instance.

        Parameters:
        - value: The name value to be validated.

        Returns:
        - The validated name value.

        Raises:
        - serializers.ValidationError: Raised if the name already exists.
        """

        if models.BillingProfile.objects.filter(
                name__iexact=value
        ).exclude(
            pk=self.instance.pk
        ).exists():
            raise serializers.ValidationError(
                'Name already exists.',
                code='exists'
            )

        return value


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BillingProfile

        fields = '__all__'

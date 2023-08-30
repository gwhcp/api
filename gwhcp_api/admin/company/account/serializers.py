from django.contrib.sites import models as site_models
from rest_framework import serializers

from admin.company.account import models


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company

        fields = '__all__'

    def update(self, instance, validated_data):
        """
        Updates the profile of a company.

        Parameters:
        - instance (object): The instance of the company profile to be updated.
        - validated_data (dict): The validated data for updating the profile.

        Returns:
        - company (object): The updated instance of the company profile.
        """

        company = super(ProfileSerializer, self).update(instance, validated_data)
        company.save()

        site_models.Site.objects.filter(pk=instance.pk).update(name=company.name)

        return company

from django_iban.validators import iban_validator, swift_bic_validator
from rest_framework import serializers

from bluebottle.bluebottle_drf2.serializers import PrivateFileSerializer
from bluebottle.utils.serializers import AddressSerializer, URLField

from .models import Organization, OrganizationDocument


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id', 'name', 'slug', 'description', 'website', 'twitter', 'facebook', 'skype')



class OrganizationDocumentSerializer(serializers.ModelSerializer):

    file = PrivateFileSerializer()

    class Meta:
        model = OrganizationDocument
        fields = ('id', 'organization', 'file')


class ManageOrganizationSerializer(OrganizationSerializer):

    slug = serializers.SlugField(required=False)

    documents = OrganizationDocumentSerializer(many=True, source='organizationdocument_set', required=False)
    registration = PrivateFileSerializer(required=False)

    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False)
    website = URLField(required=False)
    email = serializers.EmailField(required=False)
    twitter = serializers.CharField(required=False)
    facebook = serializers.CharField(required=False)
    skype = serializers.CharField(required=False)
    legal_status = serializers.CharField(required=False)

    class Meta:
        model = Organization
        exclude = ('deleted',)

    def validate_account_iban(self, attrs, source):
        value = attrs[source]
        if value:
            iban_validator(value)
        return attrs

    def validate_account_bic(self, attrs, source):
        value = attrs[source]
        if value:
            swift_bic_validator(value)
        return attrs

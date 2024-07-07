from uuid import uuid4
from rest_framework import serializers
from .models import Organisation

class AddUserToOrganisationSerializer(serializers.Serializer):
    userId = serializers.CharField(max_length=36)

class OrganisationSerializer(serializers.ModelSerializer):
    
    org_id = serializers.CharField(max_length=36,source='id',read_only=True)
    
    class Meta:
        model = Organisation
        fields = ['org_id', 'name', 'description']

    def validate(self, data):
        errors = []
        if not data.get('name'):
            errors.append({'field': 'name', 'message': 'Name is required'})
        
        if errors:
            raise serializers.ValidationError(errors)
        return data
    
    def create(self, validated_data):
        org = Organisation.objects.create(
            id = str(uuid4()),
            **validated_data
        )
        org.user.add(self.context['user'])
        return org
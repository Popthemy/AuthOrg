from rest_framework import serializers
from .models import Organisation
from 



class OrganisationSerializer(serializers.ModelSerializer):
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

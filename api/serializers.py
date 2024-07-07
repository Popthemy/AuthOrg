from rest_framework import serializers
from .models import Organisation


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
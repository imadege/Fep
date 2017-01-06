from rest_framework import serializers
from business.models import *



class BusinessSerializer(serializers.ModelSerializer):
    user=serializers.UUIDField(required=False) #to container user uuid
    level_name=serializers.CharField(max_length=50,read_only=True)

    class Meta:
        model=Business
        fields='__all__'
        
      

class BusinessAddRemoveUserSerializer(serializers.Serializer):
    email=serializers.EmailField() #to container user email
    business=serializers.UUIDField() #to container business
    is_super_level=serializers.BooleanField(default=False)
    remove_user=serializers.BooleanField(default=False)

        
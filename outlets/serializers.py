from rest_framework import serializers
from outlets.models import *




class OutletSerializer(serializers.ModelSerializer):
    class Meta:
        model=Outlet
        fields='__all__'

           
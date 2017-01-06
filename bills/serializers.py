from rest_framework import serializers
from  orders.models import *
from  bills.models import  Bill
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin

class BillsSerializer(BulkSerializerMixin,serializers.ModelSerializer):
   
    class Meta:
        model=Bill
        fields=['id','paid_to','owner','status','status_name','bill_owner_name',
                'supplier_name','number','amount']
        
        read_only_fields=('status_name','number',)
        #list_serializer_class=BulkListSerializer

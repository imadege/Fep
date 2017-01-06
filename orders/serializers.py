from rest_framework import serializers
from  orders.models import *

from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin

class OrderSerializer(BulkSerializerMixin,serializers.ModelSerializer):
   
    class Meta:
        model=Order
        fields=['id','number','amount','product','quantity','product_name',
                'retailer_name','supplier_name','outlet_name',
                'outlet','status','status_name','price','selling_price','commission']
        
        read_only_fields = ('id','amount','number','status_name',
                          'outlet_name','retailer_name',
                          'supplier_name','product_name', 'selling_price','commission'
                          )
        
        list_serializer_class=BulkListSerializer
        #update_lookup_field='id'
        
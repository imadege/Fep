from rest_framework import serializers
from products.models import *
from drf_extra_fields.fields import Base64ImageField

from outlets.serializers import OutletSerializer



class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields='__all__'

       
        
class CategorySerializer(serializers.ModelSerializer):
    unit_name=serializers.CharField(max_length=100,read_only=True)
    group_name=serializers.CharField(max_length=100,read_only=True)
    
    class Meta:
        model=Category
        fields='__all__'
        
        
class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Unit
        fields='__all__'
        



class ProductSerializer(serializers.ModelSerializer):
    price_per_unit=serializers.DecimalField(decimal_places=2,max_digits=15)
  
    class Meta:
        model=Product
        fields=['id','name','category','unit_name','stock_level',
                'description','outlet','business','price_per_unit','market_price_per_unit',
                'selling_price',
                'commission','photo','supplier_name','category_name','is_approved','is_active',
                ]
        
       
        
        
        
    
    
        
    
        
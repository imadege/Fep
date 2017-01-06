from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework import generics

from django.db import transaction
from django.utils.decorators import method_decorator
from django.http import Http404


from orders.serializers import *
from orders.models import *
from products.models import Product

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from django.db.models import Max,Min



class OrderList(ListBulkCreateUpdateDestroyAPIView):
    """USe this same urls for GET,CREATE,UPDATE  of bulk orders.
    For upload of orders. 
    also the logged in user will be treated as the retailer 
    For Filter use:
    
    supplier,
    retailer,
    outlet,
    product,
    status,
    number,
    quantity,
    price,
    date_time_ordered,
    
    You will need all required fields for all the operations.
    
    """
    
    serializer_class=OrderSerializer
    queryset=Order.objects.all()
    
    filter_backends = (DjangoFilterBackend,)
    filter_fields = '__all__' #('status','supplier','outlet', 'retailer','product','quantity','price','date_time_ordered',)
    
    
    
    def perform_create(self, serializer):
        #customize create object
        valid_data=serializer.validated_data
        #get current max number for orders
       
        max_order=Order.objects.all().aggregate(Max('number'))
        previous_number=max_order.get('number__max')  if max_order.get('number__max') else 0
        number=int(previous_number)+1 #get next number
        #status=Status.objects.get(number=0) #get peding status
        
        for data in valid_data:

            business=self.request.user.business

            if not business:
                raise serializers.ValidationError({'retailer':"User has no business assigned"})

            data.update({'retailer':business})
            data.update({'supplier':data.get('product').business})
            data.update({'price':data.get('product').selling_price()})
            data.update({'number':number})
            data.update({'commission':data.get('product').commission()})
            data.update({'selling_price':data.get('product').selling_price()})
            #data.update({'price_per_unit':})
            
            #data.update({'status':status})
            #get Status 
            
            number=number+1 #increment number
            
        serializer.save()
        
    
        
    def allow_bulk_destroy(self, qs, filtered):
        #protect multiple deletion
        return False
    
    
        
    
    
    
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(OrderList, self).dispatch(*args, **kwargs)
  

class OrderDetail(generics.RetrieveDestroyAPIView):
    """ use this for single return  of order one order """
    
    serializer_class=OrderSerializer
    queryset=Order.objects.all()

    def get_object(self):
        try:
            return Order.objects.get(pk=self.kwargs.get('pk'))
        except Order.DoesNotExist:
            raise Http404
        
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(OrderDetail, self).dispatch(*args, **kwargs)


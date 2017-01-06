from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework import generics

from django.db import transaction
from django.utils.decorators import method_decorator
from django.http import Http404


from products.serializers import *
from products.models import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny

from utils.views import TransactionalViewMixin


class GroupList(TransactionalViewMixin,generics.ListCreateAPIView):
    serializer_class=GroupSerializer
    queryset=Group.objects.all()
    


class GroupDetail(TransactionalViewMixin,generics.RetrieveUpdateDestroyAPIView):
    serializer_class=GroupSerializer
    queryset=Group.objects.all()
        



class CategoryList(TransactionalViewMixin,generics.ListCreateAPIView):
    """Return and create categories . Filter parameters are  : group,name,unit  """
    serializer_class=CategorySerializer
    
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name','group','unit',)

    def get_queryset(self):
        return Category.objects.all()


class CategoryDetail(TransactionalViewMixin,generics.RetrieveUpdateDestroyAPIView):
    serializer_class=CategorySerializer
    queryset=Category.objects.all()

   
    
    

class UnitList(TransactionalViewMixin,generics.ListCreateAPIView):
    serializer_class=UnitSerializer
    
    def get_queryset(self):
        return Unit.objects.all()
 

class UnitDetail(TransactionalViewMixin,generics.RetrieveUpdateDestroyAPIView):
    serializer_class=UnitSerializer
    queryset=Unit.objects.all()

   
        
   
    

class ProductList(TransactionalViewMixin,generics.ListCreateAPIView):
    """ List and create products of the manufacturer. For outlets , pass example: [1,2] outlet ids in order to create
     If you need to display outlet names use the outlets roots i.e /outlets/:id/ For GET requests,;
     Filter by name,category,unit,stock_level, outlet and user """

    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name','category', 'stock_level','outlet','business','unit',)
    #permission_classes = (AllowAny,)
    
    def perform_create(self, serializer):
        #customize create object
        valid_data=serializer.validated_data
        price_per_unit=valid_data.pop('price_per_unit')
        category=valid_data.get('category')
        business=valid_data.get('business')
        #get current max number for orders
        product=serializer.save(unit=category.unit)
        #create prices
        price=Price.objects.create(price_per_unit=price_per_unit,
                                   product=product,business=business,created_by=self.request.user)
                
    

class ProductDetail(TransactionalViewMixin,generics.RetrieveUpdateDestroyAPIView):
    """ can also be used for partial updates and file upload  """
    
    #parser_classes = (MultiPartParser, FormParser,JSONParser)
    serializer_class=ProductSerializer
    queryset=Product.objects.all()
    
    #avoid use of patch. use PUT for full and partial updated
    #the below also restricts delete. 
    
    http_method_names=['get','put','head','options'] 

    def put(self, request, pk, format=None):
        
        product= self.get_object()
        serializer = ProductSerializer(product,data=request.data,partial=True)
       
        if serializer.is_valid():
            valid_data=serializer.validated_data
            
            serializer.save() #save product
            
            
            previous_price=product.price_per_unit
            
            current_price=valid_data.get('price_per_unit',previous_price)
            if current_price !=previous_price:
                Price.objects.filter(product=product,user=product.user).update(is_active=False)
                Price.objects.create(price_per_unit=current_price,product=product,user=product.user)
            
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
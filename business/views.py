from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework import generics
from django.db import transaction
from django.utils.decorators import method_decorator
from django.http import Http404
from business.serializers import *
from business.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import serializers
from users.models import User



class BusinessList(generics.ListCreateAPIView):

    """ List and create Businesss. you may pass extra field 'user' 
    to create business related to the user. and make user the admin while creating
    do these for admin owners of the business only.   
    """
    serializer_class=BusinessSerializer
    queryset=Business.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name','reference_number', 'registration_number','physical_address','level',)    
        
    def perform_create(self,serializer):
        #link user to this Business
        data=serializer.validated_data
        
        #if user is given, register as admin of the business if no other admin, else just assign.
        user=data.pop('user',None)

        if user:
            try:
                user=User.objects.get(id=user)
            except:
                #user not found
                raise serializers.ValidationError({'user':"User not found "})
            #register user against Business
            #check if user already has Business
            if user.business:
                raise serializers.ValidationError({'user':"User already has business assigned"})

            business=serializer.save(level=user.level)
            user.business=business
            user.is_super_level=True #make admin of the business
            user.save()

        else:
            #create normal business. and add user later on different view. 
            serializer.save()
        


    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(BusinessList, self).dispatch(*args, **kwargs)
  


class BusinessDetail(generics.RetrieveUpdateDestroyAPIView):
    """ 

    make changes to the business

    """

    serializer_class=BusinessSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    queryset=Business.objects.all()
    
    def perform_destroy(self,business):
        #disable instead of deleting
        business.is_deleted=True
        business.save()

    def put(self, request, pk, format=None):
        
        b= self.get_object()
        serializer = BusinessSerializer(b,data=request.data,partial=True)
       
        if serializer.is_valid():
            valid_data=serializer.validated_data
            serializer.save() #save business
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(BusinessDetail, self).dispatch(*args, **kwargs)


class BusinessAddRemoveUser(generics.CreateAPIView):

    """ Add users to the Business  .
    pass remove_user=True to remove user from business profile. 
    pass is_super_level=True to make user super level on business
    """
    serializer_class=BusinessAddRemoveUserSerializer

    def perform_create(self,serializer):
        data=serializer.validated_data
        try:
            user=User.objects.get(email=data.get('email'))
        except:
            raise serializers.ValidationError({'email':"User with this email not found"})

        business=Business.objects.get(id=data.get('business'))

        #check if user is assigned business
        if not data.get('remove_user') and user.business:
            raise serializers.ValidationError({'email':"User already has business assigned"})
        
        if data.get('remove_user'):
            user.business=None
            user.is_super_level=False
        else:
            business.level=user.level
            user.business=business 
            user.is_super_level=data.get('is_super_level')
        user.save()



    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(BusinessAddRemoveUser, self).dispatch(*args, **kwargs)
  
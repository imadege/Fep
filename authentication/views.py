from django.shortcuts import render

# Create your views here.
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status

from users.serializers import UserSerializer
from users.models import User
from .serializers import EmailAuthTokenSerializer,PhoneNumberAuthTokenSerializer,SecretKeyAuthTokenSerializer
from utils.renderers import CustomJSONRenderer

from django.db import transaction
from django.utils.decorators import method_decorator

class ObtainExpiringAuthToken(views.ObtainAuthToken):
    
    serializer_class = EmailAuthTokenSerializer
    renderer_classes = (CustomJSONRenderer, )
    
    def set_serializer_class(self,data):
        if data.get('secret_key'):
            self.serializer_class=SecretKeyAuthTokenSerializer
        elif data.get('phone_number'):
            self.serializer_class=PhoneNumberAuthTokenSerializer
        else:
            self.serializer_class=EmailAuthTokenSerializer
        
       
  
    def get_token(self,user):
        try:
            Token.objects.get(user=user).delete()
        except: #token failed delete/or not exist
            pass
        finally:
            return Token.objects.create(user=user)

       
    

    def post(self, request):
        self.set_serializer_class(data=request.data)
        serializer =self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            token=self.get_token(user=serializer.validated_data['user'])
            return Response({'token': token.key,'user':UserSerializer(token.user).data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(ObtainExpiringAuthToken, self).dispatch(*args, **kwargs)

obtain_expiring_auth_token = ObtainExpiringAuthToken.as_view()

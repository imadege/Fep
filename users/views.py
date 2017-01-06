
from rest_framework import generics
from users.serializers import *
from users.models import User,Code,ResetPassword

from django.db import transaction
from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import hashlib
import uuid
from rest_framework import serializers

import random,string

from notifications.models import Message



from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from utils.renderers import CustomJSONRenderer

from rest_framework.permissions import IsAuthenticated,AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.core.exceptions import ValidationError

from django.core.mail import send_mail




class UserList(generics.ListCreateAPIView):
    """ used for user signup """
    serializer_class=UserSerializer
    renderer_classes = (CustomJSONRenderer, )
    permission_classes = (AllowAny,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,)
    filter_fields = ('first_name','last_name','id_number','email','phone_number','business','level',)
    
    search_fields=('first_name','last_name','id_number','email','phone_number','level',)
    
    def perform_create(self,serializer):
        if self.request.user.is_authenticated():
            serializer.validated_data.update({'created_by':self.request.user.email})
        serializer.save()

    def get_queryset(self):
        return User.objects.all()
    
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserList, self).dispatch(*args, **kwargs)
  


class UserDetail(generics.RetrieveUpdateAPIView):
    """ you can also mmake partial updates using PUT. 
    if password field is provided, the password will change. but no email/ notification will be sent to User
    regarding the changes
    """

    serializer_class=UserSerializer
    parser_classes = (MultiPartParser, FormParser,JSONParser)
    
    renderer_classes = (CustomJSONRenderer, )
    
    queryset=User.objects.all()

    def get_object(self):
        try:
            return User.objects.get(pk=self.kwargs.get('pk'))
        except User.DoesNotExist:
            raise Http404
    
   
    def put(self, request, pk, format=None):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            valid_data = serializer.validated_data
            serializer.save()

            if valid_data.get('password'):
                user.set_password(valid_data.get('password'))
                user.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserDetail, self).dispatch(*args, **kwargs)
 
 
 
   

class UserSecretKey(generics.RetrieveDestroyAPIView):
    """ use this for getting and creating secret key 
    once the url /path is hit, a new secret key is created"""

    serializer_class=UserSecretKeySerializer
    #permission_classes=(IsAdminUser,)
    queryset=User.objects.all()
    renderer_classes = (CustomJSONRenderer, )
    
    permission_classes = (AllowAny,)
    
    
    def get_object(self):
        #check if user exists
        profile=User.objects.get(pk=self.kwargs.get('pk'))
        
        if not profile.secret_key:
            profile.secret_key=hashlib.sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()
            profile.save()
        return profile
      
    def delete(self, request, pk, format=None):
        profile=self.get_object()
        profile.secret_key=None
        profile.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserSecretKey, self).dispatch(*args, **kwargs)

"""
class UserUploadFiles(generics.UpdateAPIView):
    serializer_class=UserUploadFilesSerializer
    queryset=User.objects.all()
    renderer_classes = (CustomJSONRenderer, )

    def get_object(self):
        try:
            return User.objects.get(pk=self.kwargs.get('pk'))
        except User.DoesNotExist:
            raise Http404
    
        
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserUploadFiles, self).dispatch(*args, **kwargs)
 
"""



class UserChangePassword(generics.CreateAPIView):
    """To change password, enter the required fields old_password,new_password,new_password_again and user.
    user will receive an email of the notification on successful reset. Also to verify email or phone number that 
    password was set to, includ the field in your post request. 
    """
    
    serializer_class=UserChangePasswordSerializer
    
    renderer_classes = (CustomJSONRenderer, )
    error_message="All the fields are required"
    success_message="Your password was changed succesfully."
    
    
    def post(self, request,format=None):
        serializer = UserChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            old_password=valid_data.get('old_password')
            new_password=valid_data.get('new_password')
            new_password_again=valid_data.get('new_password_again')
            if new_password != new_password_again:
                #passwords do not match . fail
                self.error_message="Please enter the same password twice."
                raise serializers.ValidationError({'new_password':"Passwords do not match",
                                                   'new_password_again':"Passwords do not match"})
            
            #check if user with this password exists
            if not user.check_password(old_password):
                #not found
                self.error_message="Please enter your correct  password."
                raise serializers.ValidationError({'old_password':"Incorrect password"})
         
            #change password here also verify email if user is same.
            user.set_password(new_password)
            user.is_password_changed=True
            #if email is passed, validated email also. since user received password vial email
            if valid_data.get('email') and valid_data.get('phone_number'):
                #incorrect options for verifiyn
                raise serializers.ValidationError({'email':"Enter email or phone_number or None",
                                                   'phone_number':"Enter email or phone_number or None"})

            if user.email==valid_data.get('email'): #applies if email is unique field
                user.is_email_verified=True
            if user.phone_number==valid_data.get('phone_number'): #applies if phone number is unique field
                user.is_phone_number_verified=True
            user.save()

            #send mail
            Message.create_message(message="Password Changed successfully",recipient_address=user.email)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserChangePassword, self).dispatch(*args, **kwargs)
    
    
    

    
    
class UserResetPassword(generics.CreateAPIView):
    
    """
    Uses only POST
    email field is required.
    To reset password after email request you need:
    reset_code,new_password,email,new_password_again fields. 
    To request for a reset of password: 
    you required email field only.
    
    """
    permission_classes = (AllowAny,)
    serializer_class=UserResetPasswordSerializer
    renderer_classes = (CustomJSONRenderer, )
    error_message="Oops something went wrong"
    success_message="Success"
    

    def post(self, request,format=None):
        serializer = UserResetPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            valid_data=serializer.validated_data
            email=valid_data.get('email')
            new_password=valid_data.get('new_password')
            new_password_again=valid_data.get('new_password_again')
            reset_code=valid_data.get('reset_code')
            
            
            #check if user exists
            try:
                user=User.objects.get(email=email)
            except:
                self.error_message="Oops please check that your email is correct."
                raise serializers.ValidationError({'email':"User with this email Does not exist !"})
            
            if reset_code:
                #check if code exists.
                try:
                    rp= ResetPassword.objects.filter(user=user).latest('date_created')
                except:
                    raise serializers.ValidationError({'reset_code':"Invalid or Expired reset code ."})
                
                #check if codes match
                if rp.reset_code != reset_code:
                    raise serializers.ValidationError({'reset_code':"Invalid or Expired reset code ."})
                #try reset
                if not new_password:
                    raise serializers.ValidationError({'new_password':"This requred"})
                
                if not new_password_again:
                    raise serializers.ValidationError({'new_password_again':"This requred"})
                
                if new_password != new_password_again:
                    #passwords do not match . fail
                    self.error_message="Please enter the same password twice."
                    raise serializers.ValidationError({'new_password':"Passwords do not match",
                                                   'new_password_again':"Passwords do not match"})
                
                #we reset password
                user.set_password(valid_data.get('new_password'))
                user.is_active=True
                user.save()

                #delete password reset code. 
                rp.delete()

                #remove entries
                del valid_data['new_password']
                del valid_data['new_password_again']
                self.success_message="Password reset was successful"
            else:
                #this is email reset request. we send email 
                reset_code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
                
                rp=ResetPassword.objects.create(user=user,reset_code=reset_code)
                
                

                message="We received your password reset request.Please enter %s to reset."%(reset_code)

                #send email
                #send mail
                Message.create_message(message=message,
                                       recipient_address=user.email)

                #deactivate account temporarily
                user.is_active=False
                user.save()

                self.success_message="We emailed you a password reset code."
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserResetPassword, self).dispatch(*args, **kwargs)
    
    

class UserVerifyEmail(generics.ListCreateAPIView):
    """To verify email. For sending code, use GET for veification of the code received in email use POST
    For logged in users. 
    """
    
    serializer_class=UserVerifyEmailSerializer
    
    renderer_classes = (CustomJSONRenderer, )
    error_message="All the fields are required"
    success_message="Succesfully."
    
    def get_queryset(self):
        #send email verification code for looged in use 
        user=self.request.user

        code=Code.generate(user=user,reason=Code.EMAIL_VERIFICATION)
        #send mail
        message="To verify your email enter the code : %s "%(code.code)
        Message.create_message(message=message,recipient_address=user.email)
        self.success_message='Email verification code sent.'
        return []

    
    def post(self, request,format=None):
        serializer = UserVerifyEmailSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            verification_code=valid_data.get('verification_code')
            code=Code.is_valid(user=user,reason=Code.EMAIL_VERIFICATION,code=verification_code)
            if code:
                #valid 
                user.is_email_verified=True
                user.save()
                self.success_message="Email verified"
                #remove the Code
                code.delete()


            else:
                #incorrect options for verifiyn
                raise serializers.ValidationError({'verification_code':"The code is invalid."})
                self.error_message="Please enter correct code"

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserVerifyEmail, self).dispatch(*args, **kwargs)



class UserVerifyPhoneNumber(generics.ListCreateAPIView):
    """To verify PhoneNumber. For sending code, use GET for veification of the code received in PhoneNumber use POST
    For logged in users. 
    """
    
    serializer_class=UserVerifyPhoneNumberSerializer
    
    renderer_classes = (CustomJSONRenderer, )
    error_message="All the fields are required"
    success_message="Succesfully."
    
    def get_queryset(self):
        #send email verification code for looged in use 
        user=self.request.user
        code=Code.generate(user=user,reason=Code.PHONE_NUMBER_VERIFICATION)
      
        message="%s"%(code.code)
        Message.create_message(message=message,recipient_address=user.phone_number,message_type=2)
        self.success_message='Phone Number verification code sent.'
        return []


    
    def post(self, request,format=None):
        serializer = UserVerifyPhoneNumberSerializer(data=request.data)
        if serializer.is_valid():
            valid_data=serializer.validated_data
            #chec if passwords match
            user=request.user

            verification_code=valid_data.get('verification_code')
            code=Code.is_valid(user=user,reason=Code.PHONE_NUMBER_VERIFICATION,code=verification_code)
            if code:
                #valid 
                user.is_phone_number_verified=True
                user.save()
                self.success_message="Phone Number verified"
                #remove the Code
                code.delete()
                

            else:
                #incorrect options for verifiyn
                raise serializers.ValidationError({'verification_code':"The code is invalid."})
                self.error_message="Please enter correct code"

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(UserVerifyPhoneNumber, self).dispatch(*args, **kwargs)

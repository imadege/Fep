from rest_framework import serializers
from users.models import User
from notifications.models import Message
from drf_extra_fields.fields import Base64ImageField
import random
import string


class UserSerializer(serializers.ModelSerializer):
    level_name=serializers.CharField(max_length=50,read_only=True)
    class Meta:
        model=User
        exclude=('secret_key',)
        extra_kwargs={'password':{'write_only':True}}

    def create(self,validated_data): 
        created_by=validated_data.get('created_by')
        random_password=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        email=validated_data.pop('email')

        #update created_by field

        if created_by:
            #this was added by admin
            validated_data.update({'password':random_password})
       
        #create user
        user=User.objects.create_user(email=email,
                                phone_number=validated_data.pop('phone_number'),
                                id_number=validated_data.pop('id_number'),
                                password=validated_data.pop('password'),**validated_data)

        #set password and send email if created by admin
        if created_by:
            
            #send email
            message="Account created. Please sign in with email address: %s and password: %s  .\
            "%(email,random_password)

            Message.create_message(message=message,recipient_address=email)

        return user

class UserSecretKeySerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('secret_key',)
    

        
class UserChangePasswordSerializer(serializers.Serializer):
    #user=serializers.CharField(max_length=200,write_only=True)
    old_password=serializers.CharField(max_length=50,write_only=True)
    new_password=serializers.CharField(max_length=50,write_only=True)
    new_password_again=serializers.CharField(max_length=50,write_only=True)
    phone_number=serializers.CharField(max_length=100,required=False)
    email=serializers.CharField(max_length=100,required=False)

    
   
class UserResetPasswordSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=50,write_only=True)
    reset_code=serializers.CharField(max_length=50,required=False)
    new_password=serializers.CharField(max_length=50,required=False)
    new_password_again=serializers.CharField(max_length=50,required=False)
    

class UserVerifyEmailSerializer(serializers.Serializer):
    verification_code=serializers.CharField(max_length=50,write_only=True)
   
class UserVerifyPhoneNumberSerializer(serializers.Serializer):
    verification_code=serializers.CharField(max_length=50,write_only=True)
   

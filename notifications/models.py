from django.db import models
"""
 send_mail('Password Change Done ','Password Change done.',settings.EMAIL_HOST_USER ,[user.email],
                      fail_silently=False)
            
"""
# Create your models here.
from django.utils import timezone
from django.conf import settings


class Message(models.Model):
    MESSAGE_TYPES={1:'Email',2:'SMS'}
    MESSAGE_STATUS={0:"Un Processed",1:"Processed",2:"Successful",3:"Failed"}
    MESSAGE_PRIORITY={1:"Very Urgent",2:"Urgent",3:"Normal"}
    message=models.CharField(max_length=320)
    priority=models.SmallIntegerField(default=3) #takes emails by default
    message_type=models.SmallIntegerField(default=1) #takes emails by default
    message_status=models.SmallIntegerField(default=0) #takes emails by default
    delivery_response=models.CharField(max_length=100,null=True)
    request_id=models.CharField(max_length=300,null=True)
    sender_address=models.CharField(max_length=100)
    recipient_address=models.CharField(max_length=100)
    date_created=models.DateTimeField(default=timezone.now)
    last_updated=models.DateTimeField(default=timezone.now)
    
    @classmethod
    def create_message(cls,message,recipient_address,message_type=1,sender_address=settings.EMAIL_HOST_USER):
       return  cls.objects.create(message=message,message_type=message_type,
        sender_address=sender_address,recipient_address=recipient_address)
                           
    
   
    
    

    
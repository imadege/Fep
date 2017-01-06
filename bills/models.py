from django.db import models
from django.utils import timezone
from users.models import User
    
import uuid
from business.models import Business

class Bill(models.Model):
    STATUS_CODES={0:"Pending",1:"Paid"}
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    paid_to=models.ForeignKey(Business,related_name='bill_paid')
    owner=models.ForeignKey(Business,related_name='bill_owner')
    status=models.SmallIntegerField(default=0)
    number=models.IntegerField(unique=True,help_text="Bill Number")
    amount=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    date_time_created=models.DateTimeField(default=timezone.now)

    def supplier_name(self):
        return self.paid_to.name
    
    def bill_owner_name(self):
        return self.owner.name

    def status_name(self):
        return self.STATUS_CODES.get(self.status)
    
    

    
    
    
    
    
    
        
    
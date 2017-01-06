from django.db import models
from django.utils import timezone

from users.models import User

from business.models import Business
 
class Outlet(models.Model):
    name=models.CharField(max_length=100)
    location=models.CharField(max_length=100)
    business=models.ForeignKey(Business)
    
   
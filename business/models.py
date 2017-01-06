from django.db import models
import uuid


class Business(models.Model):

    BUSINESS_LEVELS={0:"Uknown",1:"Administrator",2:"Staff",3:"Manufacturer/Supplier",4:"Retailer"}


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=200,unique=True)
    reference_number=models.CharField(max_length=100,null=True) #when live, disable null
    registration_number=models.CharField(max_length=200,unique=True,help_text="Of the business")
    description=models.CharField(max_length=200,help_text="describe the business")
    physical_address=models.CharField(max_length=200)
    certificate=models.ImageField(upload_to='business_certificates/%Y/%m/%d/',null=True)
    national_id_photo=models.ImageField(upload_to='national_id_photos/%Y/%m/%d/',null=True)
    kra_pin_certificate=models.ImageField(upload_to='kra_pins/%Y/%m/%d/',null=True)
    is_deleted=models.BooleanField(default=False)
    level=models.IntegerField(help_text="business types",default=0)
    

    @property
    def level_name(self):
        return self.BUSINESS_LEVELS.get(self.level)

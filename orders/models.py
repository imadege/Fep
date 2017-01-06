from django.db import models
from django.utils import timezone
from users.models import User
from products.models import Product
from bills.models import Bill
from outlets.models import Outlet
from business.models import Business

 
class Order(models.Model):
    STATUS_CODES={0:"Pending",1:"Initial",2:"Pending At JHL",3:"Pending at Supplier",4:"Ready For Dispatch",5:"Delivered",6:"Cancelled"}
    supplier=models.ForeignKey(Business,related_name='supplier')
    retailer=models.ForeignKey(Business,related_name='retailer')
    outlet=models.ForeignKey(Outlet)
    bill = models.ForeignKey(Bill, related_name="bill",null=True)
    product=models.ForeignKey(Product)
    status=models.SmallIntegerField() #models.ForeignKey(Status)
    number=models.IntegerField(unique=True,help_text="Order Number")
    quantity=models.IntegerField()
    price=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    commission=models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    selling_price = models.DecimalField(max_digits=20,decimal_places=2,default=0.00)
    date_time_ordered=models.DateTimeField(default=timezone.now)
    
    
    def supplier_name(self):
        return self.supplier.name

    def retailer_name(self):
        return self.retailer.name

    
    def product_name(self):
        return self.product.name
    
    def outlet_name(self):
        return self.outlet.name
            
    def status_name(self):
        return self.STATUS_CODES.get(self.status)
    
    def amount(self):
        return self.selling_price*self.quantity
    
    

    
    
    
    
    
    
        
    
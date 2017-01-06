from django.db import models
from django.utils import timezone

from users.models import User
from outlets.models  import Outlet

from business.models import Business

class Group(models.Model):
    name=models.CharField(max_length=100,unique=True,help_text="E.g Electronics, Households")
    
    
class Unit(models.Model):
    name=models.CharField(max_length=100,unique=True,help_text="Such as Kgs,Litres e.t.c")
    

class Category(models.Model):
    name=models.CharField(max_length=100,unique=True,help_text="Categories such as Unga,Laptop,Phone ")
    group=models.ForeignKey(Group)
    unit=models.ForeignKey(Unit)
    
    def unit_name(self):
        return self.unit.name
    
    def group_name(self):
        return self.group.name
    
    
    
 
class Product(models.Model):
    name=models.CharField(max_length=100,help_text="E.g Unga Hostess 2kg. ")
    category=models.ForeignKey(Category)
    unit=models.ForeignKey(Unit)
    stock_level=models.IntegerField(help_text='No. of products in store')
    photo=models.ImageField(upload_to='product_images/%Y/%m/%d/',null=True)
    description=models.CharField(max_length=100,null=True)
    outlet=models.ManyToManyField(Outlet)
    business=models.ForeignKey(Business)


    def category_name(self):
        return self.category.name
    
    def outlet_name(self):
        return self.outlet.name
    
    def price_per_unit(self): #when created. do not use as selling price.
        price=Price.objects.filter(product=self).first()
        return price.price_per_unit

    def market_price_per_unit(self): #for price active product price.
        price=Price.get_market_price(self)
        if price:
            return price.price_per_unit
        return None

    def selling_price(self): #final selling cost after commission inclusion
        market_price=self.market_price_per_unit()
        commission=self.commission()
        if market_price and commission:
            return market_price+((commission*market_price)/100)
        else:
            return None


    def commission(self): 
        price=Price.get_market_price(self)
        if price:
            return price.commission
        return None


    def is_approved(self):
        price=Price.get_market_price(self)
        return True if price else False

    def is_active(self):
        price=Price.get_market_price(self)
        return True if price else False

    def supplier_name(self):
        return self.business.name

    def unit_name(self):
        return self.unit.name



class Price(models.Model):
    price_per_unit=models.DecimalField(decimal_places=2,max_digits=12)
    commission=models.IntegerField(default=0,help_text='% age commission for calculating selling price ')
    product=models.ForeignKey(Product)
    date_created=models.DateTimeField(default=timezone.now)
    is_active=models.BooleanField(default=False)
    is_approved=models.BooleanField(default=False)
    business=models.ForeignKey(Business)
    created_by=models.ForeignKey(User)

    
    class Meta:
        ordering=['-date_created']

    @classmethod
    def get_market_price(cls,product):#return the price that is active and approved for use.
        price=cls.objects.filter(is_active=True,is_approved=True,product=product).first()
        return price

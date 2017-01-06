from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
import uuid
import random,string
from business.models import Business


class User(AbstractBaseUser):
    USER_LEVELS={1:"Administrator",2:"Staff",3:"Manufacturer/Supplier",4:"Retailer"}

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    password=models.CharField(max_length=300)
    level=models.IntegerField(help_text="Codes of 1 to 4 for different user types",default=4)
    is_superuser=models.BooleanField(default=False)
    is_super_level=models.BooleanField(default=False)
    id_number=models.CharField(max_length=50,unique=True)
    phone_number=models.CharField(max_length=20,unique=True)
    email=models.EmailField(max_length=200,unique=True)
    reference_number=models.CharField(max_length=100,null=True) #when live, disable null
    secret_key=models.CharField(max_length=300,null=True)
    is_email_verified=models.BooleanField(default=False)
    is_password_changed=models.BooleanField(default=False)
    is_phone_number_verified=models.BooleanField(default=False)
    created_by=models.CharField(max_length=100,null=True) 
    business=models.ForeignKey(Business,null=True)
    
    objects=UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number','id_number']
    
    class Meta:
        verbose_name=_('user')
        verbose_name_plural=_('users')
        
        
    def get_full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()
    
    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name
    
    @property
    def level_name(self):
        return self.USER_LEVELS.get(self.level)
    
class ResetPassword(models.Model):
    user=models.ForeignKey(User)
    reset_code=models.CharField(max_length=100)
    date_created=models.DateTimeField(default=timezone.now)
    
    
    
class Code(models.Model): #used for verifications
    #code reasons
    EMAIL_VERIFICATION=1
    PHONE_NUMBER_VERIFICATION=2


    user=models.ForeignKey(User)
    code=models.CharField(max_length=100)
    reason=models.SmallIntegerField()
    date_created=models.DateTimeField(default=timezone.now)

    @classmethod
    def generate(cls,user,reason):
        #generate general for now
        code=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        return cls.objects.create(user=user,code=code,reason=reason)
            
    @classmethod
    def is_valid(cls,user,reason,code):
        #verify if code is valid for user action
        try:
            return cls.objects.filter(user=user,reason=reason,code=code).first()
        except:
            return False

    
    
    
    
    
    
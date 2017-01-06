from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework import generics

from django.db import transaction
from django.utils.decorators import method_decorator
from django.http import Http404


from outlets.serializers import *
from outlets.models import *


from django_filters.rest_framework import DjangoFilterBackend


class OutletList(generics.ListCreateAPIView):
    """List or create manufacturer outlets for their products
    required fields are # name,location,user """
    serializer_class=OutletSerializer
    queryset=Outlet.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('name', 'location','business')
    
    
    
    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(OutletList, self).dispatch(*args, **kwargs)
  

class OutletDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=OutletSerializer
    queryset=Outlet.objects.all()

    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(OutletDetail, self).dispatch(*args, **kwargs)

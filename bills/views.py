from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser,JSONParser
from rest_framework import generics

from django.db import transaction
from django.utils.decorators import method_decorator
from django.http import Http404

from bills.serializers import  BillsSerializer
from bills.models import  Bill
from orders.models import Order

from django_filters.rest_framework import DjangoFilterBackend
from utils.renderers import CustomJSONRenderer
from rest_framework.permissions import  IsAuthenticated, AllowAny
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView

from django.db.models import Max,Min
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
import json

class BillList(generics.ListCreateAPIView):
    """USe this same urls for GET,CREATE,UPDATE  of Bills.
      For Filter use:

      paid_to,
      owner,
      status,
      number,
      amount,
      You will need all required fields for all the operations.

      """

    filter_backends = (DjangoFilterBackend,)
    filter_fields = '__all__'  # ('status','supplier','outlet', 'retailer','product','quantity','price','date_time_ordered',)
    serializer_class = BillsSerializer
    queryset = Bill.objects.all()

    def perform_create(self, serializer):
        # customize create object
        valid_data = serializer.validated_data
        # get current max number for orders

        max_order = Bill.objects.all().aggregate(Max('number'))
        previous_number = max_order.get('number__max') if max_order.get('number__max') else 0
        number = int(previous_number) + 1  # get next number
        # status=Status.objects.get(number=0) #get peding statu

        number = number + 1  # increment number
        serializer.save(number = number)



    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(BillList, self).dispatch(*args, **kwargs)


class BillDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BillsSerializer
    queryset = Bill.objects.all()

    def get_object(self):
        try:
            return Bill.objects.get(pk=self.kwargs.get('pk'))
        except Bill.DoesNotExist:
            raise Http404

    @method_decorator(transaction.atomic)
    def dispatch(self, *args, **kwargs):
        return super(BillDetail, self).dispatch(*args, **kwargs)



class Aggregate(APIView):

    permission_classes = (AllowAny,)
    success_message = "All orders updates"
    error_message = "Error"

    def post(self, request):
        orders = request.data
        aggregated_orders = {}
        supplier = 0
        total_amount  = 0
        for o in orders:
            if o['status'] !=3:
                self.error_message = "Only orders pending at supplier are to be aggregated"
                return Response(orders,400)
            else:
                total_amount = total_amount + o["price"]
                aggregated_orders.update(o)
        #Create Bill
        bill = Bill()
        bill.paid_to = request.user.business

        """ change the owner to meaningful owner """
        bill.owner = request.user.business #changed from #1


        bill.amount = total_amount
        bill.status = 0
        bill.number = self.generate_num()
        bill.save()

        #update orders
        for a in aggregated_orders:
            o = Order.objects.get(pk=a['id'])
            o.status = 4
            o.bill = bill
            o.save()

        return  Response(aggregated_orders)


    def get(self, request):
        return Response({"sdas:sasd"})


    def generate_num(self):
        max_order = Bill.objects.all().aggregate(Max('number'))
        previous_number = max_order.get('number__max') if max_order.get('number__max') else 0
        number = int(previous_number) + 1  # get next number
        return  number


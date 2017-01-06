from django.conf.urls import url

from bills.views import *

from rest_framework.routers import DefaultRouter



urlpatterns=[
            url('^$',BillList.as_view(),
                 name='bills_list'),
            url('^aggregate', Aggregate.as_view(),
                 name='aggregate'),
            url('^(?P<pk>[0-9]+)/$',BillDetail.as_view(),
                name='bill_detail'),

             ]

             


from django.conf.urls import url

from orders.views import *

urlpatterns=[
            url('^$',OrderList.as_view(),
                 name='order_list'),
            url('^(?P<pk>[0-9]+)/$',OrderDetail.as_view(),
                name='order_detail'),        
             ]

             


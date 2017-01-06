from django.conf.urls import url

from outlets.views import *

urlpatterns=[
            url('^$',OutletList.as_view(),
                 name='outlet_list'),
            url('^(?P<pk>[0-9]+)/$',OutletDetail.as_view(),
                name='outlet_detail'), 
             
                
             ]
             


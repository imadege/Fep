from django.conf.urls import url

from business.views import *

urlpatterns=[
            url('^$',BusinessList.as_view(),
                 name='business_list'), 

            url('^add-remove-user/$',BusinessAddRemoveUser.as_view(),
                 name='business_add_remove_user'),  
            url('^(?P<pk>[a-zA-Z0-9-]+)/$',BusinessDetail.as_view(),
                name='business_detail'),

             ]
             


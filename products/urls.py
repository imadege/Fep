from django.conf.urls import url

from products.views import *

urlpatterns=[
            url('^groups/$',GroupList.as_view(),
                 name='group_list'),
            url('^groups/(?P<pk>[0-9]+)/$',GroupDetail.as_view(),
                name='group_detail'), 
             
            url('^categories/$',CategoryList.as_view(),
                 name='category_list'),
            url('^categories/(?P<pk>[0-9]+)/$',CategoryDetail.as_view(),
                name='category_detail'), 
             
             
            url('^units/$',UnitList.as_view(),
                 name='unit_list'),
            url('^units/(?P<pk>[0-9]+)/$',UnitDetail.as_view(),
                name='unit_detail'), 
                
            url('^products/$',ProductList.as_view(),
                 name='product_list'),
            url('^products/(?P<pk>[0-9]+)/$',ProductDetail.as_view(),
                name='product_detail'),           
             ]
             


"""fep_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin

from authentication.views import obtain_expiring_auth_token 
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='JHL System API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^authenticate/',obtain_expiring_auth_token),
    url(r'^business/', include('business.urls',namespace='business')),
    
    url(r'^users/', include('users.urls',namespace='users')),
    url(r'^products/', include('products.urls',namespace='products')),
    #url(r'^', include('products.urls',namespace='products')),
    url(r'^outlets/', include('outlets.urls',namespace='outlets')),
    url(r'^orders/', include('orders.urls',namespace='orders')),
    url(r'^bills/', include('bills.urls',namespace='bills')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_docs.urls')),
    url(r'^swag-docs/$', schema_view)
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



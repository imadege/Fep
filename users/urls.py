from django.conf.urls import url

from users.views import *

urlpatterns=[
            url('^$',UserList.as_view(),
                 name='user_list'),
            url('^(?P<pk>[a-zA-Z0-9-]+)/secret-key/$',UserSecretKey.as_view(),
                name='user_secret_key'),
            url('^change-password/$',UserChangePassword.as_view(),
                name='change_password'),
            url('^reset-password/$',UserResetPassword.as_view(),
                name='reset_password'),

            url('^verify-email/$',UserVerifyEmail.as_view(),
                name='verify_email'),

            url('^verify-phone-number/$',UserVerifyPhoneNumber.as_view(),
                name='verify_phone_number'),


            url('^(?P<pk>[a-zA-Z0-9-]+)/$',UserDetail.as_view(),
                name='user_detail'),
             ]

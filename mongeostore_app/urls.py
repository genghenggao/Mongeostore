'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2020-08-27 21:02:36
LastEditors: henggao
LastEditTime: 2022-05-13 10:18:46
'''
from django.urls import include, path
# import routers
from rest_framework import routers

# import everything from views
from .views import *
# 添加RegisterView视图
from .views import RegisterView, CheckUsername, CheckEmail, CheckMobile, LoginViewTest, UploadInfoView
from . import views
from rest_framework.compat import re_path
from django.views.generic import TemplateView
# jwt内部实现的登陆视图
from rest_framework_jwt.views import obtain_jwt_token


from django.conf.urls import  url

# define the router
router = routers.DefaultRouter()

# define the router path and viewset to be used
router.register(r'userinfo', UserInfoViewSet)

# specify URL Path for rest_framework
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    # path('send_sms/', views.send_sms)
    path('send_sms/', MobileCountView.as_view(), name='send_sms'),
    path('username/', CheckUsername.as_view(), name='username'),
    path('email/', CheckEmail.as_view(), name='email'),
    path('mobile/', CheckMobile.as_view(), name='mobile'),
    # path('smscode/', CheckSmscode.as_view(), name='smscode'),
    path('register/', RegisterView.as_view(), name='register'),
    path('userlogin/', LoginViewTest.as_view(), name='login'),
    path(r"login", obtain_jwt_token),

    path('', TemplateView.as_view(template_name="index.html")),

    re_path(r'.*', TemplateView.as_view(template_name='index.html')),
    path('uploadfile/', views.upload_file),
    # path('test/', views.test),
    path('testinfo/', views.test,name="test"),
    path('uploadinfo/', UploadInfoView.as_view(), name='uploadinfo'),
]

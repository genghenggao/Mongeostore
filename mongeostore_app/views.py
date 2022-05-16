'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2020-08-26 18:15:34
LastEditors: henggao
LastEditTime: 2022-05-13 10:21:52
'''
from inspect import ArgSpec
from bson import ObjectId
import os
from datetime import datetime
from django.http import request
from gridfs import *
import gridfs
from django.http import JsonResponse
# from .models import UploadFile
from . import models
from rest_framework import status
from rest_framework.versioning import URLPathVersioning
from rest_framework.response import Response
import uuid
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from _datetime import datetime
import pymongo
from pymongo import MongoClient
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, login
from django.db import DatabaseError
import re
from django.http.response import HttpResponse
from utils.tencent.sms import send_sms_single
import random
from mongeostore_v1 import settings
from django.shortcuts import redirect, render
from django.views import View
from django import http
from utils.response_code import RETCODE
from rest_framework import viewsets
# import local data
from .serializers import UploadInfoSerializer, UserInfoSerializer
# from .serializers import UserInfoSerializer,SmscodeSerializer
from .models import UploadInfo, UserInfo, SmsCode
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from utils import encrypt
# create a viewset


class UserInfoViewSet(viewsets.ModelViewSet):
    # define queryset
    queryset = UserInfo.objects.all()

    # specify serializer to be used
    serializer_class = UserInfoSerializer


class CheckUsername(View):
    def get(self, request):
        # 1.根据用户名，查询用户数量
        username = self.request.GET.get('username')  # 字符串类型
        count = UserInfo.objects.filter(username=username).count()
        # 这个取值为了方便前端Login登录校验使用
        # user = UserInfo.objects.get(username=username)
        # password = user.password
        # 2. 返回响应
        data = {
            "count": count,
            # "password": password,
        }
        print(data)
        return http.JsonResponse(data)


class CheckEmail(View):
    def get(self, request):
        # 1.根据邮箱，查询用户数量
        email = self.request.GET.get('email')  # 字符串类型
        count = UserInfo.objects.filter(email=email).count()

        # 2. 返回响应
        data = {
            "count": count
        }
        print(data)
        return http.JsonResponse(data)


User = get_user_model()


class CheckMobile(View):
    def get(self, request):
        # 1.根据手机号，查询用户数量
        mobile = self.request.GET.get('mobile')  # 字符串类型
        count = UserInfo.objects.filter(mobile=mobile).count()

        # 2. 返回响应
        data = {
            "count": count
        }
        print(data)
        return http.JsonResponse(data)


class MobileCountView(View):

    """检测短信模板是否有问题"""
    # serializer_class = SmscodeSerializer

    def get(self, request):
        tpl = self.request.GET.get('tpl')
        print(tpl)
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError("短信模板错误")

        """检测手机号码是否重复"""
        mobile = self.request.GET.get('mobile')  # 字符串类型

        if UserInfo.objects.filter(mobile=mobile).count():
            raise ValidationError("手机号已经注册过，请重新输入")

        # 生成短信验证码
        code = random.randrange(1000, 9999)

        # 发送短信
        sms = send_sms_single(mobile, template_id, [code, ])
        if sms["result"] != 0:
            raise ValidationError("短信发送失败，{}".format['errmsg'])

        # 验证码写入mongodb
        '''
        MongoDB 2.2 引入一个新特性–TTL 集合，TTL集合支持失效时间设置，或者在某个特定时间;

        集合自动清除超时文档，者用来保存一个诸如session会话信息的时候非常有用。

        如果想使用TTL集合，用用到 expireAfterSeconds 选项.
        '''

        client = settings.MongoDB_client
        db = client['用户数据管理子系统']
        collection = db['用户手机注册']
        # collection = client.django_example.mongeostore_app_smscode
        collection.create_index(
            [("time", pymongo.ASCENDING)], expireAfterSeconds=66)
        data = {
            "mobile": mobile,  # 注意这个存入的类型，这样传入的是字符串str
            "code": code,

        }
        collection.insert(data)
        return http.JsonResponse({'error_massage': "ok", 'code': RETCODE.OK, })


class RegisterView(View):
    """
      注册视图
      /api/register
      """

    def get(self, request):
        """
        凡是来访问这个视图的请求, 就返回注册页面
        :param request: 请求注册页面
        :return: 注册页面
        """
        # return render(request, 'index.html')
        print(request.POST)
        return http.JsonResponse({'error_massage': "ok", 'code': RETCODE.OK, })

    def post(self, request):

        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        password = self.request.POST.get('password')
        password2 = self.request.POST.get('password2')  # 前端已经校验了
        mobile = self.request.POST.get('mobile')
        smscode = self.request.POST.get('smscode')
        # allow = request.POST.get('allow') #是否同意协议
        print(username)
        print(email)
        print(password)
        print(mobile)
        print(password2)
        print(smscode)  # 2916"}
        # 为了防止爬虫，后端需要再一次校验信息
        # 判断参数是否齐全
        if not all([username, email, password, password2, mobile, smscode]):
            # all方法,对于列表或元祖内的任意一个元素为false,则返回false,空            列表或空元祖或任意元素不为false,则返回Ture
            return http.HttpResponseForbidden("缺少必传参数")

        """检测用户名是否重复"""
        if not re.match(r"^[a-zA-Z0-9_-]{5,20}$", username):
            return http.HttpResponseForbidden("请输入5-20个字符的用户名")
        if UserInfo.objects.filter(username=username).count():
            raise ValidationError("该用户名已经注册过，请重新输入")

        """检测邮箱是否重复"""
        if not re.match(r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", email):
            return http.HttpResponseForbidden("请输入有效邮箱")
        if UserInfo.objects.filter(email=email).count():
            raise ValidationError("该邮箱已经注册过，请重新输入")
        """检测密码"""
        #  判断密码是否是6 - 20个数字
        if not re.match(r"^[a-zA-Z0-9_-]{6,20}$", password):
            return http.HttpResponseForbidden("请输入6-20位的密码")
            # 判断两次密码是否一致
        if password != password2:
            return http.HttpResponseForbidden('两次输入的密码不一致')
        md5_password = encrypt.md5(password)  # 使用MD5密文
        print("密文密码：" + md5_password)

        """检测手机号"""
        # 判断手机号是否合法Info
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return http.HttpResponseForbidden('请输入正确的手机号码')
        if UserInfo.objects.filter(mobile=mobile).count():
            raise ValidationError("该手机已经注册过，请重新输入")

        """检测验证码"""
        # client = MongoClient("192.168.55.110", 27017)
        # collection = client.mobilecode.expire
        client = settings.MongoDB_client
        db = client['用户数据管理子系统']
        collection = db['用户手机注册']
        # collection = client.django_example.mongeostore_app_smscode
        code_mobile = self.request.POST.get("mobile")
        print(type(code_mobile))  # str
        print(code_mobile)
        mongo_code = collection.find_one({"mobile": code_mobile})

        print(mongo_code)
        if not mongo_code:
            data = {
                "status_code": 500,
            }
            # return http.JsonResponse("验证码失效，或未发送，请重新发送！", data)
            return http.JsonResponse(data)
            # raise ValidationError("验证码失效，或未发送，请重新发送！")
        mongo_str_code = str(mongo_code['code'])
        print(mongo_str_code)  # 4981
        print(type(mongo_str_code))  # <class 'str'>
        print(smscode)
        print(type(smscode))  # <class 'str'>
        # 这个验证码还有点问题，申请的腾讯一天只能10条
        if smscode != mongo_str_code:
            data = {
                "status_code": 501,
            }

            return http.JsonResponse(data)
            # raise ValidationError("验证码错误，请重新输入")
        # 保存注册数据
        try:
            userInfo = UserInfo.objects.create(
                username=username, email=email, password=md5_password, mobile=mobile)
        except DatabaseError:
            return render(request, 'index.html', {'register_errmsg': '注册失败'})

        return HttpResponse('welcome!{}'.format(username))
        # return username


class LoginViewTest(APIView):
    def get(self, request):
        # return render(request, "login.html")
        return render(request, "https://www.baidu.com/")

    @csrf_exempt
    def post(self, request):
        # 1. 获取参数
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        print(username)
        # 2. 判断参数是否齐全
        if not all([username, password, ]):

            data = {
                "status_code": 502
            }
            return http.JsonResponse(data)

        # 2.1 用户名格式校验
        if not re.match(r"^[a-zA-Z0-9_-]{5,20}$", username):

            data = {
                "status_code": 502
            }
            return http.JsonResponse(data)

         # 2.2  判断密码是否是6 - 20个数字
        if not re.match(r"^[a-zA-Z0-9_-]{6,20}$", password):

            data = {
                "status_code": 503
            }
            return http.JsonResponse(data)

        # 2.3 校验用户名和密码的正确性
        if not UserInfo.objects.filter(username=username).count():
            data = {
                "status_code": 502
            }
            return http.JsonResponse(data)

        username = username.strip()
        md5_password = encrypt.md5(password)  # 使用MD5密文

        try:
            user = UserInfo.objects.get(username=username)
            if user.password == md5_password:
                # return redirect('/index.html')
                data = {
                    "status_code": 200
                }
                # return HttpResponse("Welcome,{}".format(md5_password), data)
                return http.JsonResponse(data)
            else:
                message = "密码不正确！"
                data = {
                    "status_code": 503
                }

                return http.JsonResponse(data)
        except:
            message = "用户名不存在！"
            return HttpResponse(message)

        return HttpResponse("优雅的返回")


class LoginView(APIView):
    """
    登录接口
    """

    def post(self, request, *args, **kwargs):

        # 基于jwt的认证
        # 1.去数据库获取用户信息
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        user = models.UserInfo.objects.filter(**request.data).first()
        if not user:
            return Response({'code': 1000, 'error': '用户名或密码错误'})

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return Response({'code': 1001, 'data': token})


#  上传文件到gridfs

client = settings.MongoDB_client
# client = MongoClient("192.168.92.145", 20000)  # 连接MongoDB数据库
db = client.segyfile  # 选定数据库，设定数据库名称为segyfile


def upload_file(request, *args, **kwargs):
  # 上传文件到GridFS集合中
    # 存储文件到mongo
    print("走过这里")
    if request.method == "GET":
        myFile = request.FILES.get("file", None)  # 获取上传的文件，如果没有文件，则默认为None
        print("经过这里")
        if not myFile:
            return HttpResponse("no files for upload!")
        return HttpResponse("no files for upload!")


class UploadInfoView(APIView):
    def get(self, request, *args, **kwargs):
        """
        docstring
        """
        # define queryset
        queryset = UploadInfo.objects.all()
        # specify serializer to be used
        serializer_class = UploadInfoSerializer

    def post(self, request):
        # 1>校验数据
        # form = UserInfoSerializer(request.POST)

        # 2>创建数据
        # 接收前端表单数据,使用Post.get()方法
        name = self.request.POST.get('name')  # 字符串类型
        count = UploadInfo.objects.filter(name=name).count()
        # return http.JsonResponse("Welcome to use get")
        # return HttpResponse("welcome to use get")
        data = {
            "count": count
        }
        print(data)
        return http.JsonResponse(data)


def test(request):
    if request.method == 'get':
        print("Welcome to visit")
        return Response("You are Welcome")

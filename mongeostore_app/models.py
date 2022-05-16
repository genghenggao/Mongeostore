'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2020-08-26 18:15:34
LastEditors: henggao
LastEditTime: 2022-05-13 10:17:46
'''

from djongo import models
from _datetime import datetime
# mongeostore #

class UserInfo(models.Model):
    # 使用Djongo的Model、由于官方文档还没有类似Django中的AbstractUser
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    email = models.EmailField(
        verbose_name='邮箱', max_length=32, unique=True, null=True, blank=True)
    # 设置允许为空，因为前端登录只有一个值，是username，所以mobile可以为空
    mobile = models.CharField(
        verbose_name='手机号', max_length=32, unique=True, null=True, blank=True)
    password = models.CharField(verbose_name='密码', max_length=32)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class SmsCode(models.Model):
    """"验证码"""
    mobile = models.CharField(verbose_name='手机号', max_length=32)
    smscode = models.CharField(verbose_name='验证码', max_length=8)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "手机验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
class UploadInfo(models.Model):
    '''
    上传文件
    '''
    name = models.CharField(max_length=255)
    upload_date = models.DateTimeField()
    path = models.CharField(max_length=255)
    md5 = models.CharField(max_length=33, default='')
    size = models.CharField(max_length=30, default=0)

    
    class Meta:
        verbose_name = "上传数据"
        verbose_name_plural = verbose_name

    def __str__(self): 
        return self.name
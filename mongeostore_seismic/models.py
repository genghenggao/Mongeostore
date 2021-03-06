'''
Description: henggao_learning
version: v1.0.0
Author: henggao
Date: 2020-12-16 21:36:57
LastEditors: henggao
LastEditTime: 2022-05-12 10:11:57
'''
from datetime import datetime
from django.db import models
from mongoengine import connect
from mongoengine.document import Document
from mongoengine.fields import DateTimeField, FileField, ImageField, StringField
from mongeostore_v1 import local_settings
# Create your models here.

# 设置数据库
mongos_host = local_settings.mongos_host
mongos_port = local_settings.mongos_port
connect(alias='default', db='地震数据管理子系统',
        host=mongos_host, port=mongos_port)
connect(alias='seismic_system', db='地震数据管理子系统',
        host=mongos_host, port=mongos_port) #地震数据
connect(alias='seiAcquisition_system', db='地震数据管理子系统',
        host=mongos_host, port=mongos_port)  #地震采集数据
connect(alias='seiprocess_system', db='地震数据管理子系统',
        host=mongos_host, port=mongos_port)  #地震处理数据
connect(alias='seiInterpretation_system', db='地震数据管理子系统',
        host=mongos_host, port=mongos_port)  #地震解释数据
connect(alias='seihistorical_system', db='地震数据管理子系统',
        host=mongos_host, port=mongos_port)  #地震历史数据
connect(alias='remote_system', db='遥感数据管理子系统',
        host=mongos_host, port=mongos_port)
connect(alias='logging_system', db='测井数据管理子系统',
        host=mongos_host, port=mongos_port)
connect(alias='geological_system', db='地质数据管理子系统',
        host=mongos_host, port=mongos_port)
connect(alias='hydrological_system', db='水文数据管理子系统',
        host=mongos_host, port=mongos_port)

class SeismicInfo(Document):
    '''地震数据上传'''
    seismic_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    seismic_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField()
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'seismic_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '地震勘探数据管理', 'indexes': [{'fields': ['$seismic_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.seismic_filename


class SeiAcquisitionInfo(Document):
    '''地震采集数据上传'''
    seiAcquisition_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    seiAcquisition_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='seiAcquisition_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'seiAcquisition_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '地震采集数据', 'indexes': [{'fields': ['$seiAcquisition_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.seiAcquisition_filename
class SeiprocessInfo(Document):
    '''地震处理数据上传'''
    seiprocess_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    seiprocess_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='seiprocess_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'seiprocess_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '地震处理数据', 'indexes': [{'fields': ['$seiprocess_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.seiprocess_filename
class SeiInterpretationInfo(Document):
    '''地震解释数据上传'''
    seiInterpretation_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    seiInterpretation_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='seiInterpretation_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'seiInterpretation_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '地震解释数据', 'indexes': [{'fields': ['$seiInterpretation_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.seiInterpretation_filename
class SeihistoricalInfo(Document):
    '''地震历史数据'''
    seihistorical_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    seihistorical_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='seihistorical_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'seihistorical_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '地震历史数据', 'indexes': [{'fields': ['$seihistorical_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.seihistorical_filename


class RemoteInfo(Document):
    '''遥感数据上传'''
    remote_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    remote_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='remote_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'remote_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '遥感影像管理', 'indexes': [{'fields': ['$remote_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.remote_filename


class LoggingInfo(Document):
    '''测井数据上传'''
    logging_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    logging_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='logging_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'logging_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '测井数据管理', 'indexes': [{'fields': ['$logging_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.logging_filename


class GeologicalInfo(Document):
    '''地质数据上传'''
    geological_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    geological_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='geological_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'geological_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '地质数据管理', 'indexes': [{'fields': ['$geological_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.geological_filename


class HydrologicalInfo(Document):
    '''水文数据上传'''
    hydrological_filename = StringField(required=True)
    location = StringField(required=True)
    company_name = StringField(required=True)
    uploader = StringField(required=True)
    hydrological_upload_date = DateTimeField(default=datetime.now(), required=True)
    project_name = StringField(required=True)
    filedata = FileField(db_alias='hydrological_system', collection_name='fs')
#     seismicprofile = ImageField(collection_name='seismicprofile')
#     filedata = FileField(collection_name='test')  # 设置Gridfs中的存储桶名称

    meta = {'db_alias': 'hydrological_system',
            # 'collection': '地震数据Demo1', 'indexes': ['filename']}
            'collection': '水文数据管理', 'indexes': [{'fields': ['$hydrological_filename', "$location"],
                                               'default_language': 'english',
                                               'weights': {'title': 10, 'content': 2}
                                               }]}

    def __str__(self) -> str:
        """
        docstring
        """
        return self.hydrological_filename
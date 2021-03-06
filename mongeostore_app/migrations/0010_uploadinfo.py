# Generated by Django 3.0.5 on 2020-10-23 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mongeostore_app', '0009_smscode'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('upload_date', models.DateTimeField()),
                ('path', models.CharField(max_length=255)),
                ('md5', models.CharField(default='', max_length=33)),
                ('size', models.CharField(default=0, max_length=30)),
            ],
            options={
                'verbose_name': '上传数据',
                'verbose_name_plural': '上传数据',
            },
        ),
    ]

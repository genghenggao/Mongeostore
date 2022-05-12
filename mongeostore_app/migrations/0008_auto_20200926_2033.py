# Generated by Django 3.0.5 on 2020-09-26 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mongeostore_app', '0007_auto_20200910_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(blank=True, max_length=32, null=True, unique=True, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='mobile',
            field=models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='手机号'),
        ),
    ]
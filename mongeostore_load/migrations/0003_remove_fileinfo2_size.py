# Generated by Django 3.0.5 on 2020-10-28 18:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mongeostore_load', '0002_auto_20201027_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileinfo2',
            name='size',
        ),
    ]

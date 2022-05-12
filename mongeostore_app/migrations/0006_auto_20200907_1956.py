# Generated by Django 3.0.5 on 2020-09-07 11:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mongeostore_app', '0005_auto_20200903_1709'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('content', models.CharField(max_length=200)),
                ('created', models.DateTimeField()),
                ('port', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='mobile',
            field=models.CharField(max_length=32, unique=True, verbose_name='手机号'),
        ),
    ]
# Generated by Django 3.0.5 on 2020-08-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mongeostore_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mysegy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_id', models.CharField(max_length=50, verbose_name='编号')),
                ('x_line', models.FloatField()),
                ('y_line', models.FloatField()),
                ('value', models.FloatField()),
                ('author', models.CharField(max_length=10, verbose_name='记录人员')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

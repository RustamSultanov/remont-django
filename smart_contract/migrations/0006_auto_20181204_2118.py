# Generated by Django 2.1.4 on 2018-12-04 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0005_auto_20181204_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useraccept',
            name='accept',
        ),
        migrations.RemoveField(
            model_name='useraccept',
            name='failure',
        ),
    ]

# Generated by Django 2.1.4 on 2018-12-05 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0006_auto_20181204_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccept',
            name='imp',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
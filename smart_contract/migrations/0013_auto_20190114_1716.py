# Generated by Django 2.1.4 on 2019-01-14 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0012_auto_20190114_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messegesappeal',
            old_name='comment',
            new_name='appeal',
        ),
    ]

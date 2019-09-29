# Generated by Django 2.1.4 on 2018-12-10 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smart_contract', '0009_remove_useraccept_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccept',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(1, 'Ужасно'), (2, 'Плохо'), (3, 'Нормально'), (4, 'Хорошо'), (5, 'Отлично')], default=5),
        ),
    ]

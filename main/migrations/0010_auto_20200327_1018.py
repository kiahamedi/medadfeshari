# Generated by Django 2.2.10 on 2020-03-27 10:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_auto_20190531_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myidea',
            name='idea_published',
            field=models.DateTimeField(default=datetime.datetime(2020, 3, 27, 10, 18, 8, 155784), verbose_name='date published'),
        ),
    ]

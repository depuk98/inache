# Generated by Django 3.2.7 on 2024-01-04 09:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0035_auto_20231222_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrolefactory',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 1, 1, 0, 0)),
            preserve_default=False,
        ),
    ]

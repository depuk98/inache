# Generated by Django 3.2.7 on 2023-08-21 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_auto_20230821_1221'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseusermodel',
            name='language',
            field=models.JSONField(default=None, null=True),
        ),
    ]

# Generated by Django 3.2.7 on 2023-08-09 09:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_auto_20230809_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auditlog',
            name='uploaded_by',
        ),
        migrations.RemoveField(
            model_name='uploadedfile_s3',
            name='created_by',
        ),
    ]

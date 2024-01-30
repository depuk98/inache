# Generated by Django 3.2.7 on 2023-02-16 07:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auditlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='created_at',
            field=models.CharField(blank=True, default=django.utils.timezone.localtime, max_length=500),
        ),
        migrations.AlterField(
            model_name='case',
            name='CaseNumber',
            field=models.CharField(blank=True, max_length=50, unique=True),
        ),
    ]

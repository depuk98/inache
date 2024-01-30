# Generated by Django 3.2.7 on 2024-01-22 07:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0039_alter_userrolefactory_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='Date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='case',
            name='Time',
            field=models.CharField(blank=True, default=django.utils.timezone.now, max_length=500),
        ),
    ]
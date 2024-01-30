# Generated by Django 3.2.7 on 2023-08-30 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_auto_20230825_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='CaseNature',
            field=models.CharField(choices=[('Complaint', 'Complain'), ('Query', 'Query'), ('Suggestion', 'Suggestion')], default='Complaint', max_length=64),
        ),
    ]

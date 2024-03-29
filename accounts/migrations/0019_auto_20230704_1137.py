# Generated by Django 3.2.7 on 2023-07-04 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20230703_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auditlog',
            name='status',
            field=models.CharField(choices=[('Assigned to Reporter', 'Assigned To Reporter'), ('Reassigned to Reporter', 'Reassigned To Reporter'), ('Assigned to Manager', 'Assigned To Manager'), ('Reassigned to Manager', 'Reassigned To Manager'), ('Assigned to Troubleshooter', 'Assigned To Troubleshooter'), ('Under Investigation', 'Under Investigation'), ('Resolved', 'Resolved'), ('Re Investigation', 'Re Investigation'), ('Closed', 'Closed'), ('Assigned to Quality Checker', 'Assigned To Quality Checker'), ('Completed', 'Completed')], max_length=64),
        ),
        migrations.AlterField(
            model_name='case',
            name='CaseStatus',
            field=models.CharField(choices=[('Assigned to Reporter', 'Assigned To Reporter'), ('Reassigned to Reporter', 'Reassigned To Reporter'), ('Assigned to Manager', 'Assigned To Manager'), ('Reassigned to Manager', 'Reassigned To Manager'), ('Assigned to Troubleshooter', 'Assigned To Troubleshooter'), ('Under Investigation', 'Under Investigation'), ('Resolved', 'Resolved'), ('Re Investigation', 'Re Investigation'), ('Closed', 'Closed'), ('Assigned to Quality Checker', 'Assigned To Quality Checker'), ('Completed', 'Completed')], default='Assigned to Reporter', max_length=64),
        ),
    ]

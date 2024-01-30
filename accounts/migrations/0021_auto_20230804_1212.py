# Generated by Django 3.2.7 on 2023-08-04 06:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0020_auto_20230707_1814'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('CR', 'Case Reporter'), ('CM', 'Case Manager'), ('CT', 'Case Troubleshooter'), ('FACTORY_ADMIN', 'Factory Admin'), ('SUPER_ADMIN', 'Super Admin'), ('INACHE_ADMIN', 'Inache Admin'), ('DEFAULT_ROLE', 'Default Role')], default='DEFAULT_ROLE', max_length=64, unique=True)),
                ('group_permissions', models.ManyToManyField(to='auth.Group')),
            ],
        ),
        migrations.AlterModelOptions(
            name='baseusermodel',
            options={'permissions': (('view_awareness_program', 'view awareness program'), ('add_awareness_program', 'add awareness program'), ('change_awareness_program', 'change awareness program'), ('view_broadcast_message', 'view broadcast message'), ('add_broadcast_message', 'add broadcast message'), ('change_broadcast_message', 'change broadcast message'), ('crud_factory_admin', 'crud factory admin'), ('crud_cr', 'crud case reporter'), ('crud_cm', 'crud case manager'), ('crud_ct', 'crud case troubleshooter'))},
        ),
        migrations.CreateModel(
            name='UserRoleFactory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('factory_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.factory')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.role')),
                ('user_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(to='auth.Permission')),
            ],
            options={
                'unique_together': {('user_fk', 'role', 'factory_fk')},
            },
        ),
        
        migrations.AlterField(
            model_name='case',
            name='CaseManager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases_m', to='accounts.userrolefactory'),
        ),
        migrations.AlterField(
            model_name='case',
            name='CaseReporter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases_r', to='accounts.userrolefactory'),
        ),
        migrations.AlterField(
            model_name='case',
            name='CaseTroubleShooter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cases_t', to='accounts.userrolefactory'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='uploaded_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.userrolefactory'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='status',
            field=models.CharField(choices=[('Assigned to Reporter', 'Assigned To Reporter'), ('Reassigned to Reporter', 'Reassigned To Reporter'), ('Assigned to Manager', 'Assigned To Manager'), ('Reassigned to Manager', 'Reassigned To Manager'), ('Assigned to Troubleshooter', 'Assigned To Troubleshooter'), ('Under Investigation', 'Under Investigation'), ('Resolved', 'Resolved'), ('Re Investigation', 'Re Investigation'), ('Closed', 'Closed'), ('Assigned to Quality Checker', 'Assigned To Quality Checker'), ('Completed', 'Completed'), ('Unreponsive', 'Unresponsive'), ('Approved', 'Approved')], max_length=64),
        ),
        migrations.AlterField(
            model_name='case',
            name='CaseStatus',
            field=models.CharField(choices=[('Assigned to Reporter', 'Assigned To Reporter'), ('Reassigned to Reporter', 'Reassigned To Reporter'), ('Assigned to Manager', 'Assigned To Manager'), ('Reassigned to Manager', 'Reassigned To Manager'), ('Assigned to Troubleshooter', 'Assigned To Troubleshooter'), ('Under Investigation', 'Under Investigation'), ('Resolved', 'Resolved'), ('Re Investigation', 'Re Investigation'), ('Closed', 'Closed'), ('Assigned to Quality Checker', 'Assigned To Quality Checker'), ('Completed', 'Completed'), ('Unreponsive', 'Unresponsive'), ('Approved', 'Approved')], default='Assigned to Reporter', max_length=64),
        ),
        migrations.AddField(
            model_name='uploadedfile_s3',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cretby', to='accounts.userrolefactory'),
        ),
        migrations.AlterField(
            model_name='auditlog',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cretbyal', to=settings.AUTH_USER_MODEL),
        ),
        
        
    ]


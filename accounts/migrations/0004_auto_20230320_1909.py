# Generated by Django 3.2.7 on 2023-03-20 13:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20230216_1313'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baseusermodel',
            options={'permissions': (('view_awareness_program', 'view awareness program'), ('add_awareness_program', 'add awareness program'), ('change_awareness_program', 'change awareness program'), ('view_broadcast_message', 'view broadcast message'), ('add_broadcast_message', 'add broadcast message'), ('change_broadcast_message', 'change broadcast message'), ('view_holiday_calender', 'view holiday calender'), ('add_holiday_calender', 'add holiday calender'), ('change_holiday_calender', 'change holiday calender'), ('crud_factory_admin', 'crud factory admin'), ('crud_cr', 'crud case reporter'), ('crud_cm', 'crud case manager'), ('crud_ct', 'crud case troubleshooter'))},
        ),
        migrations.AlterModelOptions(
            name='case',
            options={'permissions': (('change_CaseDetails', 'can change CaseDetails'),)},
        ),
        migrations.AddField(
            model_name='baseusermodel',
            name='company_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.company'),
        ),
        migrations.AddField(
            model_name='baseusermodel',
            name='created_by',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='baseusermodel',
            name='factory_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.factory'),
        ),
        migrations.AddField(
            model_name='complainer',
            name='Gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], default='Others', max_length=15),
        ),
        migrations.AddField(
            model_name='complainer',
            name='Language',
            field=models.CharField(choices=[('English', 'English'), ('Hindi', 'Hindi'), ('Kannada', 'Kannada'), ('Punjabi', 'Punjabi')], default='English', max_length=20),
        ),
        migrations.AddField(
            model_name='factory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='factory',
            name='last_modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='baseusermodel',
            name='role',
            field=models.CharField(choices=[('CR', 'Case Reporter'), ('CM', 'Case Manager'), ('CT', 'Case Troubleshooter'), ('FACTORY_ADMIN', 'Factory Admin'), ('SUPER_ADMIN', 'Super Admin'), ('INACHE_ADMIN', 'Inache Admin'), ('DEFAULT_ROLE', 'Default Role')], default='DEFAULT_ROLE', max_length=64),
        ),
        migrations.AlterField(
            model_name='factory',
            name='Code',
            field=models.CharField(default='', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='factorynumber',
            name='Company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.company'),
        ),
        migrations.AlterField(
            model_name='factorynumber',
            name='Factory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.factory'),
        ),
    ]

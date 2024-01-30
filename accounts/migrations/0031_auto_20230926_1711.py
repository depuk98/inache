# Generated by Django 3.2.7 on 2023-09-26 11:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_auto_20230920_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrolefactory',
            name='factory_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.factory'),
        ),
        migrations.CreateModel(
            name='FactoryRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=100)),
                ('last_modified', models.DateTimeField(blank=True, default=django.utils.timezone.localtime)),
                ('Company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.company')),
            ],
        ),
        migrations.AddField(
            model_name='factory',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.factoryregion'),
        ),
        migrations.AddField(
            model_name='userrolefactory',
            name='region_fk',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.factoryregion'),
        ),
    ]

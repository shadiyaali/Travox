# Generated by Django 5.1.4 on 2024-12-23 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0003_banking_delete_bankaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_number', models.CharField(blank=True, max_length=11, null=True)),
                ('invoice_date', models.DateField()),
                ('terms', models.CharField(choices=[('Next 15', 'Next 15'), ('Next 30', 'Next 30'), ('Due on Receipt', 'Due on Receipt'), ('Due end of the month', 'Due end of the month')], max_length=255)),
                ('due_date', models.DateField()),
                ('quotation_no', models.IntegerField()),
                ('lpo_number', models.TextField(blank=True, null=True)),
                ('lpo_date', models.DateField(blank=True, null=True)),
                ('subject', models.TextField()),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('notes', models.TextField(blank=True, null=True)),
                ('customer_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='superadmin.users')),
                ('item', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='superadmin.subscription')),
                ('sales_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='superadmin.staff')),
            ],
        ),
    ]
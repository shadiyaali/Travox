# Generated by Django 5.1.4 on 2024-12-23 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0002_bankaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(max_length=20, unique=True)),
                ('account_holder_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('branch_name', models.CharField(blank=True, max_length=100, null=True)),
                ('ifsc_code', models.CharField(blank=True, max_length=11, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='BankAccount',
        ),
    ]

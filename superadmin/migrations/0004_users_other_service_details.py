# Generated by Django 5.1.4 on 2024-12-23 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('superadmin', '0003_staff'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='other_service_details',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
# Generated by Django 4.2.17 on 2024-12-25 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farm_management', '0003_milkproduction_recorded_by_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cow',
            unique_together=set(),
        ),
    ]

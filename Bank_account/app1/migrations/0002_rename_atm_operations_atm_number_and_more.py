# Generated by Django 5.0.6 on 2024-05-23 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operations',
            old_name='atm',
            new_name='atm_number',
        ),
        migrations.RenameField(
            model_name='operations',
            old_name='client',
            new_name='card_number',
        ),
    ]

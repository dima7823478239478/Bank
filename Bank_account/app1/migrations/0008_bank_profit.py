# Generated by Django 5.0.6 on 2024-07-30 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_operations_add_take'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='profit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]
# Generated by Django 5.0.7 on 2024-11-21 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_total_earnings_account_total_earnings'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='affliate_commision',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='account',
            name='total_withdrawal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]

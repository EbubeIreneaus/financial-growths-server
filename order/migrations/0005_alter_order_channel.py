# Generated by Django 5.0.7 on 2024-08-14 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_alter_investment_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='channel',
            field=models.CharField(blank=True, choices=[('BTC', 'BTC'), ('USDT', 'USDT'), ('MEMO', 'MEMO')], max_length=20, null=True),
        ),
    ]

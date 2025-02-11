# Generated by Django 5.0.7 on 2024-08-14 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_alter_order_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='channel',
            field=models.CharField(blank=True, choices=[('BTC', 'BTC'), ('USDT(TRC20)', 'USDT TRC20'), ('ETH', 'ETHEREUM'), (' USDT(ERC20)', 'USDT ERC20')], max_length=20, null=True),
        ),
    ]

# Generated by Django 5.0.7 on 2024-07-30 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_investment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='investment',
            name='plan',
            field=models.CharField(choices=[('bronze', 'BRONZE'), ('silver', 'SILVER'), ('gold', 'GOLD'), ('vip', 'VIP')], max_length=20),
        ),
    ]

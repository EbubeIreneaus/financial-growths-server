# Generated by Django 5.0.7 on 2024-11-20 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_rename_end_date_investment_last_profit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investment',
            name='status',
        ),
        migrations.AlterField(
            model_name='investment',
            name='last_profit',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]

# Generated by Django 5.0.7 on 2024-11-20 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_alter_investment_plan'),
    ]

    operations = [
        migrations.RenameField(
            model_name='investment',
            old_name='end_date',
            new_name='last_profit',
        ),
        migrations.AddField(
            model_name='investment',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='investment',
            name='plan',
            field=models.CharField(choices=[('starter', 'Starter'), ('basic', 'Basic'), ('silver', 'Silver'), ('gold', 'Gold'), ('r-estate', 'Real Estate')], max_length=20),
        ),
    ]

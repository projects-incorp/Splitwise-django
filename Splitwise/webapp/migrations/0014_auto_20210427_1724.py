# Generated by Django 3.1.6 on 2021-04-27 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0013_auto_20210427_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction_pairs',
            name='amount',
            field=models.FloatField(null=True),
        ),
    ]
# Generated by Django 3.0.2 on 2020-10-25 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_auto_20201025_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='support_model',
            name='customer_id',
            field=models.IntegerField(null=True),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-16 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trial50', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
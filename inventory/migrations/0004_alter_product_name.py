# Generated by Django 4.2.7 on 2023-11-19 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0003_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(choices=[('Concealer', 'Concealer'), ('Mascara', 'Mascara'), ('Blush', 'Blush'), ('Foundation', 'Foundation'), ('Eye shadow', 'Eye shadow'), ('Eye liner', 'Eye liner'), ('Primer', 'Primer'), ('Clinique', 'Clinique'), ('Bronzer', 'Bronzer'), ('Highlighter', 'Highlighter'), ('Maybelline', 'Maybelline'), ('Powder', 'Powder'), ('Mosturizer', 'Mosturizer'), ('Cream', 'Cream'), ('Shampoo', 'Shampoo')], max_length=255),
        ),
    ]

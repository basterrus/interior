# Generated by Django 3.2.9 on 2021-11-06 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='productcategory',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]

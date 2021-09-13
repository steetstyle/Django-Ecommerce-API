# Generated by Django 3.1.13 on 2021-09-13 19:37

from django.db import migrations, models
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_auto_20210913_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='product.productmedia'),
        ),
    ]

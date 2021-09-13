# Generated by Django 3.1.13 on 2021-09-12 16:03

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models
import django.db.models.deletion
import project.core.db.fields
import project.core.utils.editorjs


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('description', project.core.db.fields.SanitizedJSONField(blank=True, null=True, sanitizer=project.core.utils.editorjs.clean_editor_js)),
                ('background_image_alt', models.CharField(blank=True, max_length=128)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('slug', models.SlugField(allow_unicode=True, max_length=255, unique=True)),
                ('description', project.core.db.fields.SanitizedJSONField(blank=True, null=True, sanitizer=project.core.utils.editorjs.clean_editor_js)),
                ('description_plaintext', models.TextField(blank=True)),
                ('search_vector', django.contrib.postgres.search.SearchVectorField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('charge_taxes', models.BooleanField(default=True)),
                ('rating', models.FloatField(blank=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category')),
            ],
            options={
                'ordering': ('slug',),
            },
        ),
        migrations.CreateModel(
            name='ProductMedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_order', models.IntegerField(db_index=True, editable=False, null=True)),
                ('alt', models.CharField(blank=True, max_length=128)),
                ('type', models.CharField(choices=[('IMAGE', 'An uploaded image or an URL to an image'), ('VIDEO', 'A URL to an external video')], default='IMAGE', max_length=32)),
                ('external_url', models.CharField(blank=True, max_length=256, null=True)),
                ('oembed_data', models.JSONField(blank=True, default=dict)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='product.product')),
            ],
            options={
                'ordering': ('sort_order', 'pk'),
            },
        ),
        migrations.AddIndex(
            model_name='product',
            index=django.contrib.postgres.indexes.GinIndex(fields=['search_vector'], name='product_pro_search__e78047_gin'),
        ),
    ]
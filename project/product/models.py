import os

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import JSONField  # type: ignore
from django.db.models import (
    Q,
    TextField,
)
from mptt.managers import TreeManager
from mptt.models import MPTTModel

from project.core.utils.draftjs import json_content_to_raw_text
from project.core.utils.editorjs import clean_editor_js
from project.core.db.fields import SanitizedJSONField
from project.core.models import SortableModel


from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel


from . import ProductMediaTypes


def get_category_image_path(instance, filename):
    return os.path.join(f'category/{str(instance.id)}', str(instance.id), filename)

class Category(MPTTModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = SanitizedJSONField(blank=True, null=True, sanitizer=clean_editor_js)
    parent = models.ForeignKey(
        "self", null=True, blank=True, related_name="children", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to=get_category_image_path, blank=True, null=True)
    background_image_alt = models.CharField(max_length=128, blank=True)

    objects = models.Manager()
    tree = TreeManager()

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('parent'),
        FieldPanel('background_iamge'),
        FieldPanel('background_image_alt'),
        ImageChooserPanel('image')
    ]

    def __str__(self) -> str:
        return self.name


def get_product_image_path(instance, filename):
    return os.path.join(f'product/{str(instance.id)}', str(instance.id), filename)

class Product(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = SanitizedJSONField(blank=True, null=True, sanitizer=clean_editor_js)
    description_plaintext = TextField(blank=True)
    search_vector = SearchVectorField(null=True, blank=True)
    image = models.ImageField(upload_to=get_product_image_path, blank=True, null=True)
    category = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    updated_at = models.DateTimeField(auto_now=True, null=True)
    charge_taxes = models.BooleanField(default=True)
  
    rating = models.FloatField(null=True, blank=True)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('description_plaintext'),
        FieldPanel('search_vector'),
        FieldPanel('category'),
        ImageChooserPanel('image')
    ]

    class Meta:
        app_label = "product"
        ordering = ("slug",)
        indexes = [GinIndex(fields=["search_vector"])]

    def __repr__(self) -> str:
        class_ = type(self)
        return "<%s.%s(pk=%r, name=%r)>" % (
            class_.__module__,
            class_.__name__,
            self.pk,
            self.name,
        )

    def __str__(self) -> str:
        return self.name

    @property
    def plain_text_description(self) -> str:
        return json_content_to_raw_text(self.description)

    def get_first_image(self):
        all_media = self.media.all()
        images = [media for media in all_media if media.type == ProductMediaTypes.IMAGE]
        return images[0] if images else None

    @staticmethod
    def sort_by_attribute_fields() -> list:
        return ["concatenated_values_order", "concatenated_values", "name"]


def get_product_media_image_path(instance, filename):
    return os.path.join(f'product/{str(instance.product.id)}', str(instance.id), filename)

class ProductMedia(SortableModel):
    product = models.ForeignKey(Product, related_name="media", on_delete=models.CASCADE)
    alt = models.CharField(max_length=128, blank=True)
    type = models.CharField(
        max_length=32,
        choices=ProductMediaTypes.CHOICES,
        default=ProductMediaTypes.IMAGE,
    )
    external_url = models.CharField(max_length=256, blank=True, null=True)
    oembed_data = JSONField(blank=True, default=dict)
    image = models.ImageField(upload_to=get_category_image_path, blank=True, null=True)

    panels = [
        FieldPanel('product'),
        FieldPanel('alt'),
        FieldPanel('type'),
        FieldPanel('external_url'),
        FieldPanel('oembed_data'),
        FieldPanel('category'),
        ImageChooserPanel('image')
    ]

    class Meta:
        ordering = ("sort_order", "pk")
        app_label = "product"

    def get_ordering_queryset(self):
        return self.product.media.all()




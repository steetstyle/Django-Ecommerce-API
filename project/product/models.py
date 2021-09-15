import os

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import JSONField  # type: ignore

from mptt.managers import TreeManager
from mptt.models import MPTTModel

from project.core.utils.draftjs import json_content_to_raw_text

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import RichTextField


from . import ProductMediaTypes


def get_category_image_path(instance, filename):
    return os.path.join(f'category/{str(instance.id)}', str(instance.id), filename)

class Category(MPTTModel,ClusterableModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description = RichTextField(null=True, blank=True)
    parent = ParentalKey(
         "self",
        related_name="children",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    background_image_alt = models.CharField(max_length=128, blank=True)

    objects = models.Manager()
    tree = TreeManager()

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('background_image_alt'),
        ImageChooserPanel('image')
    ]

    def __str__(self) -> str:
        return self.name


def get_product_image_path(instance, filename):
    return os.path.join(f'product/{str(instance.id)}', str(instance.id), filename)

class Product(ClusterableModel):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True)
    description =     description = RichTextField(null=True, blank=True)
    search_vector = SearchVectorField(null=True, blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    category = ParentalKey(
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

    @property
    def code(self):
        return str(self.pk)

    def get_price(self):
        return str(12)


def get_product_media_image_path(instance, filename):
    return os.path.join(f'product/{str(instance.product.id)}', str(instance.id), filename)

class ProductMedia(ClusterableModel):
    product = ParentalKey(Product, related_name="media", on_delete=models.CASCADE)
    alt = models.CharField(max_length=128, blank=True)
    type = models.CharField(
        max_length=32,
        choices=ProductMediaTypes.CHOICES,
        default=ProductMediaTypes.IMAGE,
    )
    external_url = models.CharField(max_length=256, blank=True, null=True)
    oembed_data = JSONField(blank=True, default=dict)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        InlinePanel('product'),
        FieldPanel('alt'),
        FieldPanel('type'),
        FieldPanel('external_url'),
        FieldPanel('oembed_data'),
        ImageChooserPanel('image')
    ]

    class Meta:
        ordering = ("pk",)
        app_label = "product"

    def get_ordering_queryset(self):
        return self.product.media.all()




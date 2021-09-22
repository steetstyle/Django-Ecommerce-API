
from rest_framework import serializers
from rest_framework.fields import Field
from .models import QRTable

from wagtail.images.views.serve import generate_image_url

class ImageTypeField(Field):
    """
    Serializes the "type" field of each object.

    Example:
    "type": "wagtailimages.Image"
    """
    def get_attribute(self, instance):
        return instance

    def to_representation(self, obj):
        url = generate_image_url(obj.image, 'fill-150x150')
        return url

class QRTableSerializer(serializers.ModelSerializer):
    image = ImageTypeField(read_only=True)

    class Meta:
        model = QRTable
        fields = ('pk', 'name', 'code', 'image')
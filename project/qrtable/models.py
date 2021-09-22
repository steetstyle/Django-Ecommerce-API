import uuid
import os
import requests
from io import BytesIO

import pyqrcode

from django.core.files.images import ImageFile
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image



def saveSystemCode(inClass, inCode, inPK, prefix):
    systemCode = inCode
    if not systemCode:
        systemCode = uuid.uuid4().hex[:6].upper()

    while inClass.objects.filter(code=systemCode).exclude(pk=inPK).exists():
        systemCode = uuid.uuid4().hex[:6].upper()

    return systemCode

class QRTable(models.Model):
    name = models.CharField(max_length=200)
    status = models.BooleanField(default=False)
    code = models.CharField(max_length=25, blank=True, null=True, unique=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('status'),
        FieldPanel('code'),
        ImageChooserPanel('image')
    ]

    def save(self, *args, **kwargs):
        self.code = saveSystemCode(QRTable, self.code, self.pk, "qr_")
        http_res = requests.get(f'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={self.code}')
        title = f'{self.code}.jpg'
        image_file = ImageFile(BytesIO(http_res.content), name=title)
        image = Image(title=title, file=image_file)
        image.save()
        self.image = image
        super(QRTable, self).save(*args, **kwargs)

from django.db import models
import uuid
import os
import pyqrcode


from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel

def saveSystemCode(inClass, inCode, inPK, prefix):
    systemCode = inCode
    if not systemCode:
        systemCode = uuid.uuid4().hex[:6].upper()

    while inClass.objects.filter(systemCode=systemCode).exclude(pk=inPK).exists():
        systemCode = uuid.uuid4().hex[:6].upper()

    return systemCode

def get_image_path(instance, filename):
    return os.path.join('qrs', str(instance.id), filename)

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
        #qr = pyqrcode.png(get_image_path(self,self.code))
        #self.image = qr
        super(QRTable, self).save(*args, **kwargs)

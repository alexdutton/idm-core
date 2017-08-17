import camera_imagefield
from django import forms

from . import models


class ImageForm(forms.ModelForm):
    image = camera_imagefield.CameraImageField()

    class Meta:
        model = models.Image
        fields = ('image',)

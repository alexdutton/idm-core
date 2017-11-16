import fractions

import camera_imagefield
from django import forms

from . import models


class ImageForm(forms.ModelForm):
    image = camera_imagefield.CameraImageField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field_kwargs, image_context = {}, self.instance.context
        if image_context.min_aspect_ratio_x and image_context.min_aspect_ratio_y:
            field_kwargs['min_aspect_ratio'] = fractions.Fraction(image_context.min_aspect_ratio_x,
                                                                  image_context.min_aspect_ratio_y)
        if image_context.max_aspect_ratio_x and image_context.max_aspect_ratio_y:
            field_kwargs['max_aspect_ratio'] = fractions.Fraction(image_context.max_aspect_ratio_x,
                                                                  image_context.max_aspect_ratio_y)
        if image_context.max_width and image_context.max_height:
            field_kwargs['max_size'] = (image_context.max_width, image_context.max_height)
        field_kwargs['prefer_jpeg'] = image_context.prefer_jpeg

        self.fields['image'] = camera_imagefield.CameraImageField(**field_kwargs)


    class Meta:
        model = models.Image
        fields = ('image',)

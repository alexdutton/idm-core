from rest_framework import serializers

from . import models


class ImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:image-detail')
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, instance):
        return self.context['request'].build_absolute_uri(instance.get_image_url())

    class Meta:
        model = models.Image
        fields = ('id', 'url', 'image_url', 'created', 'context_id')


class EmbeddedImageListSerializer(serializers.ListSerializer):
    def to_representation(self, data):
        return {image.context_id: self.child.to_representation(image)
                for image in data.filter(state='accepted')}


class EmbeddedImageSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='api:image-detail')
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, instance):
        return self.context['request'].build_absolute_uri(instance.get_image_url())

    class Meta:
        model = models.Image
        fields = ('id', 'url', 'image_url', 'created')
        list_serializer_class = EmbeddedImageListSerializer

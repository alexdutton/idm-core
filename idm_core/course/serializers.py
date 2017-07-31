from rest_framework import serializers

from idm_core.course import models


class TerseCourseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Course
        fields = ('id', 'label')

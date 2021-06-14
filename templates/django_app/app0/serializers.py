from rest_framework import serializers
from .models import Model0


class Model0Serializer(serializers.ModelSerializer):
    class Meta:
        model = Model0
        fields = ('id', 'name', 'description', 'value')

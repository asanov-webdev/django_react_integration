from .models import Model0
from .serializers import Model0Serializer
from rest_framework import generics


class Model0ListCreate(generics.ListCreateAPIView):
    queryset = Model0.objects.all()
    serializer_class = Model0Serializer

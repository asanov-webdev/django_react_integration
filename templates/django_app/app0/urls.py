from django.urls import path
from . import views

urlpatterns = [
    path('api/app0/', views.Model0ListCreate.as_view()),
]

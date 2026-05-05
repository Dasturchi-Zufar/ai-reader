from django.urls import path
from .views import TextToSpeechView,home,PDFToSpeechView,ImageToSpeechView

urlpatterns = [
    path('',home),
    path('read/', TextToSpeechView.as_view()),
    path('pdf/',PDFToSpeechView.as_view()),
    path('image/', ImageToSpeechView.as_view()),
]
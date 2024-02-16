from django.urls import path
from . import views

urlpatterns = [
    path('upload_anime/', views.upload_anime, name='upload_anime'),
    path('watched_anime/', views.get_watched_anime, name='watched_anime'),
]

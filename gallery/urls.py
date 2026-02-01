from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery, name='gallery'),
    path('category/<int:category_id>/', views.gallery_category, name='gallery_category'),
]
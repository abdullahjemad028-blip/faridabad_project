from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_notices, name='all_notices'),
    path('events/', views.events, name='events'),
    path('notice/<int:notice_id>/', views.notice_detail, name='notice_detail'),
]
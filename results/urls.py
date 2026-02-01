from django.urls import path
from . import views

urlpatterns = [
    path('', views.result_home, name='result_home'),
    path('check/', views.check_result, name='check_result'),
    path('view/<int:result_id>/', views.result_view, name='result_view'),
    path('exam/<int:exam_id>/', views.exam_results, name='exam_results'),
    path('guardian/login/', views.guardian_login, name='guardian_login'),
    path('guardian/logout/', views.guardian_logout, name='guardian_logout'),
    path('guardian/dashboard/', views.guardian_dashboard, name='guardian_dashboard'),
]
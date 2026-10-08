from django.urls import path
from . import views

app_name = 'teacher_portal'

urlpatterns = [
    path('', views.teacher_dashboard, name='dashboard'),
    path('class/<int:pk>/', views.teacher_class_detail, name='class_detail'),
    path('homework/', views.homework_list, name='homework_list'),
    path('homework/add/', views.homework_create, name='homework_create'),
    path('homework/<int:pk>/edit/', views.homework_edit, name='homework_edit'),
    path('homework/<int:pk>/delete/', views.homework_delete, name='homework_delete'),
    path('messages/', views.teacher_message_list, name='message_list'),
    path('messages/send/', views.teacher_message_create, name='message_create'),
    path('messages/<int:pk>/', views.teacher_message_detail, name='message_detail'),
    path('evaluations/', views.evaluation_list, name='evaluation_list'),
    path('evaluations/add/', views.evaluation_create, name='evaluation_create'),
    path('attendance/', views.attendance_view, name='attendance_view'),
    path('attendance/mark/', views.attendance_mark, name='attendance_mark'),
]

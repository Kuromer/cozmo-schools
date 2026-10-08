from django.urls import path
from . import views

app_name = 'parent_portal'

urlpatterns = [
    path('', views.parent_dashboard, name='dashboard'),
    path('fees/', views.parent_fees, name='fees'),
    path('warnings/', views.parent_warnings, name='warnings'),
    path('warnings/<int:pk>/', views.parent_warning_detail, name='warning_detail'),
    path('invitations/', views.parent_invitations, name='invitations'),
    path('homework/', views.parent_homework, name='homework'),
    path('evaluations/', views.parent_evaluations, name='evaluations'),
    path('messages/', views.parent_messages, name='messages'),
    path('messages/<int:pk>/', views.parent_message_detail, name='message_detail'),
    path('messages/new/', views.parent_message_create, name='message_create'),
    path('attendance/', views.parent_attendance, name='attendance'),
]

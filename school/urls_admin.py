from django.urls import path
from . import views

app_name = 'admin_portal'

urlpatterns = [
    path('', views.admin_dashboard, name='dashboard'),
    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('students/<int:pk>/delete/', views.student_delete, name='student_delete'),
    path('finance/', views.finance_list, name='finance_list'),
    path('finance/add/', views.fee_create, name='fee_create'),
    path('finance/<int:pk>/edit/', views.fee_edit, name='fee_edit'),
    path('finance/<int:pk>/toggle/', views.fee_toggle, name='fee_toggle'),
    path('warnings/', views.warning_list, name='warning_list'),
    path('warnings/add/', views.warning_create, name='warning_create'),
    path('warnings/<int:pk>/cancel/', views.warning_cancel, name='warning_cancel'),
    path('invitations/', views.invitation_list, name='invitation_list'),
    path('invitations/add/', views.invitation_create, name='invitation_create'),
    path('invitations/<int:pk>/update/', views.invitation_update, name='invitation_update'),
    path('reports/', views.reports, name='reports'),
    path('reports/export/', views.export_report, name='export_report'),
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_create, name='user_create'),
    path('users/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('classes/', views.class_list, name='class_list'),
    path('classes/add/', views.class_create, name='class_create'),
    path('classes/<int:pk>/edit/', views.class_edit, name='class_edit'),
    path('classes/<int:pk>/delete/', views.class_delete, name='class_delete'),
]

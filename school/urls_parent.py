from django.urls import path
from . import views

app_name = 'parent_portal'

urlpatterns = [
    path('', views.parent_dashboard, name='dashboard'),
]

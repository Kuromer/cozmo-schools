from django.contrib import admin
from django.urls import path, include
from accounts.views import redirect_after_login

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('admin-portal/', include(('school.urls_admin', 'admin_portal'))),
    path('teacher/', include(('school.urls_teacher', 'teacher_portal'))),
    path('parent/', include(('school.urls_parent', 'parent_portal'))),
    path('', redirect_after_login, name='home'),
]

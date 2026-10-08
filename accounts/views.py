from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from .forms import LoginForm

class CustomLoginView(auth_views.LoginView):
    template_name = 'registration/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

@login_required
def redirect_after_login(request):
    user = request.user
    if user.is_admin_user():
        return redirect('admin_portal:dashboard')
    elif user.is_teacher():
        return redirect('teacher_portal:dashboard')
    elif user.is_parent():
        return redirect('parent_portal:dashboard')
    return redirect('logout')

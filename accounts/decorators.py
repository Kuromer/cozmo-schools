from django.shortcuts import redirect
from django.contrib import messages as django_messages
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                django_messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def admin_required(view_func):
    return role_required(['admin'])(view_func)

def teacher_required(view_func):
    return role_required(['teacher'])(view_func)

def parent_required(view_func):
    return role_required(['parent'])(view_func)

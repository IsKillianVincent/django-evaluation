from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def dashboard_view(request):
    if request.user.is_employer:
        return redirect('employer_dashboard')
    else:
        return redirect('user_applications')

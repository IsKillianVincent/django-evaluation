from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from jobs.models.notification import Notification
from django.http import JsonResponse
from django.views.decorators.http import require_POST

@login_required
def notification_list_view(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, "jobs/notifications.html", {"notifications": notifications})

@login_required
def unread_notification_count(request):
    count = request.user.notifications.filter(is_read=False).count()
    return JsonResponse({"unread_count": count})

@require_POST
@login_required
def mark_notification_as_read_view(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({"success": True})
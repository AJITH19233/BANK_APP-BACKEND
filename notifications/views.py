from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Notification

class NotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Allow filtering by unread if ?unread=true is provided
        unread_only = request.GET.get('unread', 'false').lower() == 'true'
        notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
        if unread_only:
            notifs = notifs.filter(is_read=False)
            
        data = [{
            "id": n.id,
            "title": n.title,
            "message": n.message,
            "is_read": n.is_read,
            "created_at": n.created_at
        } for n in notifs[:20]]  # limit to last 20
        return Response(data)

class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.is_read = True
            notif.save()
            return Response({"success": True})
        except Notification.DoesNotExist:
            return Response({"error": "Not found"}, status=404)

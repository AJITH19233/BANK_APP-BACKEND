from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import Account
from transactions.models import Transaction
from notifications.models import Notification
from users.models import User

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f"dashboard_{request.user.id}"
        
        try:
            data = cache.get(cache_key)
            if data:
                return Response(data)
        except Exception as e:
            print(f"Warning: Cache get failed - {e}")
            data = None

        accounts = Account.objects.filter(user=request.user)
        transactions = Transaction.objects.filter(
            from_account__user=request.user
        ).order_by('-created_at')[:5]

        notifications = Notification.objects.filter(
            user=request.user,
            is_read=False
        )
        


        data = {
            "accounts": [
                {"account_number": a.account_number, "balance": a.balance}
                for a in accounts
            ],
            "recent_transactions": [
                {"amount": t.amount, "status": t.status}
                for t in transactions
            ],
            "notifications": [
                {"title": n.title}
                for n in notifications
            ]
        }

        try:
            cache.set(cache_key, data, timeout=30)  # cache 30 sec
        except Exception:
            pass
            
        return Response(data)

class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_superuser:
            return Response({"error": "Unauthorized. Superuser access required."}, status=403)
            
        total_users = User.objects.count()
        total_accounts = Account.objects.count()
        total_transactions = Transaction.objects.count()
        
        # Simple volume metric
        from django.db.models import Sum
        volume = Transaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0
        
        recent_trans = Transaction.objects.select_related('from_account__user', 'to_account__user').order_by('-created_at')[:10]
        
        data = {
            "metrics": {
                "total_users": total_users,
                "total_accounts": total_accounts,
                "total_transactions": total_transactions,
                "total_volume": volume
            },
            "recent_global_activity": [
                {
                    "from": t.from_account.user.username if t.from_account else "Unknown",
                    "to": t.to_account.user.username if t.to_account else "Unknown",
                    "amount": t.amount,
                    "status": t.status,
                    "date": t.created_at
                } for t in recent_trans
            ]
        }
        return Response(data)
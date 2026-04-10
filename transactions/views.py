from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer,TransferSerializer
from accounts.models import Account

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        filter_type = request.GET.get('type', 'all').lower()
        
        if filter_type == 'sent':
            transactions = Transaction.objects.filter(from_account__in=accounts)
        elif filter_type == 'received':
            transactions = Transaction.objects.filter(to_account__in=accounts)
        else:
            from django.db.models import Q
            transactions = Transaction.objects.filter(Q(from_account__in=accounts) | Q(to_account__in=accounts))
            
        transactions = transactions.select_related('from_account', 'to_account').order_by('-created_at')
        
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    

#transfer api

from django.db import transaction
import uuid
from django.core.cache import cache

class TransferMoneyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            from_acc_no = serializer.validated_data['from_account']
            to_acc_no = serializer.validated_data['to_account']
            amount = serializer.validated_data['amount']

            try:
                from_account = Account.objects.get(account_number=from_acc_no, user=request.user)
                to_account = Account.objects.get(account_number=to_acc_no)

                if from_account.balance < amount:
                    return Response({"error": "Insufficient balance"}, status=400)

                with transaction.atomic():
                    from_account.balance -= amount
                    to_account.balance += amount

                    from_account.save()
                    to_account.save()

                    Transaction.objects.create(
                        from_account=from_account,
                        to_account=to_account,
                        amount=amount,
                        transaction_type="TRANSFER",
                        status="SUCCESS",
                        reference_number=str(uuid.uuid4())
                    )
                    
                    try:
                        cache.delete(f"dashboard_{request.user.id}")
                    except Exception as e:
                        print(f"Warning: Cache deletion failed (Redis might be down) - {e}")

                return Response({"message": "Transfer successful"})

            except Account.DoesNotExist:
                return Response({"error": "Account not found"}, status=404)

        return Response(serializer.errors, status=400)
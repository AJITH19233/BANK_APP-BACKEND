import os
import django
import random
from decimal import Decimal

# Setup django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking.settings')
django.setup()

from users.models import User
from accounts.models import Account
from transactions.models import Transaction
from notifications.models import Notification

print("Cleaning up old data...")
Transaction.objects.all().delete()
Notification.objects.all().delete()
Account.objects.all().delete()
User.objects.exclude(is_superuser=True).delete()

print("Creating mock users...")
user1 = User.objects.create_user(username="alex", email="alex@example.com", password="password123", phone="555-0101")
user2 = User.objects.create_user(username="sarah", email="sarah@example.com", password="password123", phone="555-0102")
user3 = User.objects.create_user(username="demo", email="demo@example.com", password="password123", phone="555-0103")

print("Creating mock accounts...")
acc1 = Account.objects.create(user=user1, account_number="ACC-1001", balance=Decimal("15000.50"), account_type="Checking")
acc2 = Account.objects.create(user=user2, account_number="ACC-2002", balance=Decimal("4500.00"), account_type="Savings")
acc3 = Account.objects.create(user=user3, account_number="ACC-3003", balance=Decimal("25600.75"), account_type="Checking")
acc3_savings = Account.objects.create(user=user3, account_number="ACC-3004", balance=Decimal("5000.00"), account_type="Savings")

print("Creating mock transactions...")
# Alex -> Demo
Transaction.objects.create(
    from_account=acc1, to_account=acc3, amount=Decimal("150.00"), 
    transaction_type="Transfer", status="Completed", reference_number="REF-90901"
)
# Demo -> Sarah
Transaction.objects.create(
    from_account=acc3, to_account=acc2, amount=Decimal("300.00"), 
    transaction_type="Transfer", status="Completed", reference_number="REF-90902"
)
# Sarah -> Alex
Transaction.objects.create(
    from_account=acc2, to_account=acc1, amount=Decimal("50.00"), 
    transaction_type="Transfer", status="Completed", reference_number="REF-90903"
)
# Demo -> Alex
Transaction.objects.create(
    from_account=acc3, to_account=acc1, amount=Decimal("1200.00"), 
    transaction_type="Transfer", status="Pending", reference_number="REF-90904"
)

print("Creating mock notifications...")
Notification.objects.create(user=user3, title="Welcome to NexusBank!", message="Your new Checking account was created.")
Notification.objects.create(user=user3, title="Security Alert", message="New login detected from an unrecognized device.")

print("Seed data successfully injected!")

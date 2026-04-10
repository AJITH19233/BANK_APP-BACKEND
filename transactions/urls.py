from django.urls import path
from .views import TransactionListView, TransferMoneyView

urlpatterns = [
    path('', TransactionListView.as_view()),
    path('transfer/', TransferMoneyView.as_view()),
]
from django.urls import path
from .views import BeneficiaryView

urlpatterns = [
    path('', BeneficiaryView.as_view(), name='beneficiaries'),
]

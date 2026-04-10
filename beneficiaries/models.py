from django.db import models
from users.models import User

class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    beneficiary_account = models.CharField(max_length=20)
    beneficiary_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    ifsc_code = models.CharField(max_length=20)

    def __str__(self):
        return self.beneficiary_name
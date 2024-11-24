from django.db import models
from authentication.models import User

# Create your models here.
class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    active_investment = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    pending_withdraw = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    total_earnings = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    last_deposit = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    last_withdraw = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    total_withdrawal = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    affliate_commision = models.DecimalField(default=0.0, decimal_places=2, max_digits=10)
    date = models.DateField(auto_now=True)
    

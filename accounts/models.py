from django.db import models
from django.contrib.auth.models import User


class balance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField(default=0)
    is_borrower = models.BooleanField('Borrower', default=False)
    is_investor = models.BooleanField('Investor ', default=False)

    def __str__(self):
        return self.user.username
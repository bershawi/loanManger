from rest_framework import serializers
from accounts.models import balance


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = balance
        fields = ["user", "balance", "is_borrower", "is_investor"]
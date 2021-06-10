from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.models import balance
from .serializers import BalanceSerializer
from rest_framework import permissions


class BalanceDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, balance_id, user_id):

        try:
            return balance.objects.get(id=balance_id, user=user_id)
        except balance.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, balance_id, *args, **kwargs):

        balance_instance = self.get_object(balance_id, request.user.id)
        if not balance_instance:
            return Response(
                {"res": "Object with balance id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = BalanceSerializer(balance_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, balance_id, *args, **kwargs):

        balance_instance = self.get_object(balance_id, request.user.id)
        if not balance_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'balance': request.data.get('balance'),
            'is_borrower': request.data.get('is_borrower'),
            'is_investor': request.data.get('is_investor'),
            'user': request.user.id
        }
        serializer = BalanceSerializer(instance=balance_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, balance_id, *args, **kwargs):

        balance_instance = self.get_object(balance_id, request.user.id)
        if not balance_instance:
            return Response(
                {"res": "balance with balance id not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        balance_instance.delete()
        return Response(
            {"res": "Balance deleted!"},
            status=status.HTTP_200_OK
        )


class BalanceListApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):

        balances = balance.objects.filter(user=request.user.id)
        serializer = BalanceSerializer(balances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):

        data = {
            'balance': request.data.get('balance'),
            'is_borrower': request.data.get('is_borrower'),
            'is_investor': request.data.get('is_investor'),
            'user': request.user.id
        }
        serializer = BalanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from django.conf.urls import url
from django.urls import path, include
from .views import (
    BalanceDetailApiView, BalanceListApiView
)

urlpatterns = [
    path('', BalanceListApiView.as_view()),
    path('', BalanceDetailApiView.as_view()),
    path('', BalanceDetailApiView.as_view()),
    path('<int:todo_id>/', BalanceDetailApiView.as_view()),
]
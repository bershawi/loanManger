from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from .models import balance
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.messages import constants as messages


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            instance = balance(user=request.user, balance=0)
            instance.save()
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def profile(request):
    msg = ""
    if request.method == "POST":
        try:
            username = request.POST["username"]
            amount = request.POST["amount"]
            senderUser = User.objects.get(username=request.user.username)
            receiverrUser = User.objects.get(username=username)
            sender = balance.objects.get(user=senderUser)
            rate = int((sender * 15 // 100) + 3)
            receiverr = balance.objects.get(user=receiverrUser)
            if sender.is_investor:
                sender.balance = sender.balance - int(amount)
                receiverr.balance = receiverr.balance + int(amount)
            if sender.is_borrower:
                sender.balance = (rate + sender) - int(amount)
                receiverr.balance = (rate + sender) + int(amount)
            sender.save()
            receiverr.save()
            msg = "Transaction Success"
        except Exception as e:
            print(e)
            msg = "Transaction Failure, Please check and try again"
    user = balance.objects.get(user=request.user)
    return render(request, 'profile.html', {"balance": user.balance, "Borrower": user.is_borrower, "Investor": user.is_investor, "msg": msg})


def logout_request(request):
    logout(request)
    messages.INFO(request, "Logged out successfully!")
    return redirect("logout.html")

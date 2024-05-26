from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from distutils.command import upload
from moments.models import WeChatUser, Status
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


# Create your views here.
def home(request):
    return render(request, "homepage.html")


@login_required
def show_user(request):
    user = request.user
    po = {
        "name": user.username,
        "motto": "i love kungfu",
        "email": user.email,
        "region": "Shaanxi",
        "pic": "Po2.jpg",
    }

    return render(request, "user.html", {"user": po})


@login_required
def show_status(request):
    statuses = Status.objects.all()
    return render(request, "status.html", {"statuses": statuses})


@login_required
def submit_post(request):
    user = WeChatUser.objects.get(user=request.user)
    text = request.POST.get("text")
    uploaded_file = request.FILES.get("pics")
    if uploaded_file:
        name = uploaded_file.name
        with open(f"./moments/static/image/{name}", "wb") as handle:
            for block in uploaded_file.chunks():
                handle.write(block)
    else:
        name = ""
    if text:
        status = Status(user=user, text=text, pics=name)
        status.save()
        return redirect("/status")
    return render(request, "my_post.html")


@login_required
def show_friends(request):
    return render(request, "friends.html")


class LoginView(View):
    def get(self, request):
        return render(request, "homepage.html")

    def post(self, request):
        if "login" in request.POST:
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/user", {"user": user})
            else:
                return render(
                    request,
                    "homepage.html",
                    {"login_error": "Invalid username or password"},
                )
        elif "signup" in request.POST:
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            if WeChatUser.objects.filter(user__username=username).exists():
                return render(
                    request,
                    "homepage.html",
                    {"signup_error": "User already exists"},
                )
            user = User(username=username, email=email, password=password)
            user.save()
            wechat_user = WeChatUser(user=user)
            wechat_user.save()
            login(request, user)
            return redirect("/user")
        return render(request, "homepage.html")

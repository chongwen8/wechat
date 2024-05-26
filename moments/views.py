from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from distutils.command import upload
from moments.models import WeChatUser, Status


# Create your views here.
def home(request):
    return render(request, "homepage.html")

@login_required
def show_user(request):
    po = {
        "name": "xiao po",
        "motto": "i love kungfu",
        "email": "po@disney.com",
        "region": "Shaanxi",
        "pic": "Po2.jpg",
    }

    return render(request, "user.html", {'user': po})

@login_required
def show_status(request):
    statuses = Status.objects.all()
    return render(request, "status.html", {'statuses': statuses})

@login_required
def submit_post(request):
    user = WeChatUser.objects.get(user = request.user)
    text = request.POST.get('text')
    uploaded_file = request.FILES.get('pics')
    if uploaded_file:
        name = uploaded_file.name
        with open(f'./moments/static/image/{name}', 'wb') as handle:
            for block in uploaded_file.chunks():
                handle.write(block)
    else:
        name = ''
    if text:
        print(name)
        status = Status(user=user, text=text, pics=name)
        status.save()
        return redirect('/status')
    return render(request, "my_post.html")

@login_required
def show_friends(request):
    return render(request, "friends.html")
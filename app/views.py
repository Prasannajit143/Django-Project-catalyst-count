from django.shortcuts import redirect,render
from django.contrib.auth.models import User
def Home(request):
    return redirect('/accounts/login')

def welcome(request):
    return render(request, 'file_upload.html')

def query_builder(request):
    return render(request,'query_builder.html')

def users(requst):
    users = User.objects.all()
    return render(requst,'user.html',{'users': users})

def delete(requst,pk):
    user = User.objects.get(pk=pk)
    user.delete()
    return redirect('/users')

def add_user(request):
    return render(request,'add_user.html')

def save_user(requst):
    username = requst.POST.get('username')
    password = requst.POST.get('password')
    email = requst.POST.get('email')
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    new_user.save()
    return redirect('/users')
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
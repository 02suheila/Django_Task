from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate 
from django.contrib.auth import login,logout
from iq_files import settings
from django.core.mail import send_mail 

# Create your views here.
def home(request):
    return render(request,'authentication/index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        c_number = request.POST['c_number']

        if User.objects.filter(username = username):
            messages.error(request , "Username already exist! Please try some other username")
            return redirect('home')
        
        if User.objects.filter(email = email):
            messages.error(request , "Email already exist! Please try some other Email")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "password didn't match")
        
        if len(c_number)!=10:
            messages.error(request, "Enter number properly") 

        if not username.isalnum():
            messages.error(request, "Username must be alphanumric only")
            return redirect('home')
        myuser=User.objects.create_user(username , email , pass1 )
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your Account has been Successfully Created")
    return render(request,'authentication/signup.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username , password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,'authentication/index.html',{'fname' : fname})
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request,'authentication/signin.html')

def signout(request):
    logout(request)
    messages.success(request, "logged out successfully!")
    return redirect('home')

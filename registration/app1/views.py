from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from registration import settings


# Create your views here.
def home(request):
    return render(request,"app1/index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if User.objects.filter(username=username):
            messages.error(request, "Username already Exist! Please try another Username")
            return redirect("home")
        if User.objects.filter(email=email):
            messages.error(request, "Email already Registered!")
            return redirect("home")
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters")
        if pass1 != pass2:
            messages.error(request, "Password's didn't match!")
        if not username.isalnum():
            messages.error(request, "Username must be Alphe-Numeric")
            return redirect("home")
        

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been Successflly Created.")

       

        return redirect('signin')

    return render(request,"app1/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "app1/index.html", {'fname':fname})
        
        else:
            messages.error(request, "Bad Credentials!")
            return redirect("home")

    return render(request,"app1/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged Out Scuccessfully!")
    return redirect("home")
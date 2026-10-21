from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.http import     HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from.forms import RegisterForm
def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user =authenticate( request,username=username,password=password,)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        if not User.objects.filter(username=username).exists():
            return render(request, "login.html",{"error":"Invalid username"})
        return render(request, "login.html", {"error1": "Invalid password."})
       
       
       
    return render(request, "login.html")
def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        password= request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        # check username is already exists
        if User.objects.filter(username=username).exists():
            return render(request, "register.html", {"error1": "Username already exists."})
        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match."})
        # password contains at least 4 characters, one character and one number
        if len(password) < 4:
            return render(request, "register.html", {"error": "Password must be at least 4 characters long."})
         # 3. Check password contains a character
        if not any(char.isalpha() for char in password):
            return render(request, "register.html", {
                "error": "Password must contain at least one character."
            })

        # 4. Check password contains a number
        if not any(char.isdigit() for char in password):
            return render(request, "register.html", {
                "error": "Password must contain at least one number."
            })
        # Create the user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return render(request, "register.html", {"success": "Account created successfully."})
    return render(request, "register.html")
     
@login_required
def dashboard(request):
    return render(request, "dashboard.html")
def forgot_password(request):
    if request.method == "POST":
        username = request.POST["username"]
        new_password = request.POST["new_password"]
        confirm_password = request.POST["confirm_password"]

# check username is already exists
        if not User.objects.filter(username=username).exists():
            return render(request, "forgot_password.html", {"error1": "Username does not exist."})
        if new_password != confirm_password:
            return render(request, "forgot_password.html", {"error": "Passwords do not match."})
        # password contains at least 4 characters, one character and one number
        if len(new_password) < 4:
            return render(request, "forgot_password.html", {"error": "Password must be at least 4 characters long."})
         # 3. Check password contains a character
        if not any(char.isalpha() for char in new_password):
            return render(request, "forgot_password.html", {
                "error": "Password must contain at least one character."
            })

        # 4. Check password contains a number
        if not any(char.isdigit() for char in new_password):
            return render(request, "forgot_password.html", {
                "error": "Password must contain at least one number."
            })
        # Update the user's password
        user = User.objects.get(username=username)
        user.set_password(new_password)
        user.save()
        return render(request, "forgot_password.html", {"success": "Password updated successfully."})

    return render(request, "forgot_password.html")
def user_logout(request):
    logout(request)
    return redirect("login")
from django.shortcuts import render, redirect,get_object_or_404
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
            return redirect("HomePage")
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
def HomePage(request):
    return render(request, "HomePage.html")
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

def Myprofile(request):
    return render(request, 'Myprofile.html')
def saved_address(request):
    return render(request, 'saved_address.html')
def setting(request):
    return render(request,'setting.html')

def terms_conditions(request):
    return render(request, "terms_conditions.html")
def language(request):
    return render(request,'language.html')
def help(request):
    return render(request, "help.html")
def security(request):
    if request.method == "POST":
            username = request.POST["username"]
            new_password = request.POST["new_password"]
            confirm_password = request.POST["confirm_password"]
    
    # check username is already exists
            if not User.objects.filter(username=username).exists():
                return render(request, "security.html", {"error1": "Username does not exist."})
            if new_password != confirm_password:
                return render(request, "security.html", {"error": "Passwords do not match."})
            # password contains at least 4 characters, one character and one number
            if len(new_password) < 4:
                return render(request, "security.html", {"error": "Password must be at least 4 characters long."})
             # 3. Check password contains a character
            if not any(char.isalpha() for char in new_password):
                return render(request, "security.html", {
                    "error": "Password must contain at least one character."
                })
    
            # 4. Check password contains a number
            if not any(char.isdigit() for char in new_password):
                return render(request, "security.html", {
                    "error": "Password must contain at least one number."
                })
            # Update the user's password
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            return render(request, "security.html", {"success": "Password updated successfully."})
    
    return render(request, "security.html")

from categories.models import Category
from products.models import Product
def category_page(request):
    categories = Category.objects.filter(is_active=True)

    return render(
        request,
        'categories/category_list.html',
        {'categories': categories}
    )
"""""
#This code is for product access using id
def category_detail(request, category_id):
    category = get_object_or_404(
        Category,
        id=category_id,
        is_active=True
    )

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('category')

    return render(
        request,
        'categories/category_detail.html',
        {
            'category': category,
            'products': products,
        }
    )
"""
#This code is for product access using name
def category_detail(request, category_name):
    category = get_object_or_404(
        Category,
        name__iexact=category_name,
        is_active=True
    )

    products = Product.objects.filter(
        category=category,
        is_active=True
    ).select_related('category')

    return render(
        request,
        'categories/category_detail.html',
        {
            'category': category,
            'products': products,
        }
    )
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import NotificationPreference

@login_required
def notification(request):
    # Get this user's record, creating it with defaults if necessary.
    preferences, created = NotificationPreference.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        # Read checkbox values. Unchecked checkboxes are not sent by HTML.
        preferences.order_updates = (
            request.POST.get("order_updates") == "on"
        )
        preferences.offers_deals = (
            request.POST.get("offers_deals") == "on"
        )
        preferences.wishlist_alerts = (
            request.POST.get("wishlist_alerts") == "on"
        )
        preferences.personalized_recommendations = (
            request.POST.get("personalized_recommendations") == "on"
        )
        preferences.security_alerts = (
            request.POST.get("security_alerts") == "on"
        )

        preferences.email_notifications = (
            request.POST.get("email_notifications") == "on"
        )
        preferences.sms_notifications = (
            request.POST.get("sms_notifications") == "on"
        )
        preferences.push_notifications = (
            request.POST.get("push_notifications") == "on"
        )

        preferences.save()

        messages.success(
            request,
            "Your notification preferences have been saved."
        )

        return redirect("notification")

    return render(request,"notification.html",{"preferences": preferences},)

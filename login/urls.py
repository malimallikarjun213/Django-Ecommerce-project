from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_login, name="login"),
    path("register/", views.register, name="register"),
    path("HomePage/", views.HomePage, name="HomePage"),
    path("logout/", views.user_logout, name="logout"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
    path("Myprofile/",views.Myprofile, name="Myprofile"),
    path("saved_address/", views.saved_address,name="saved_address"),
    path("setting/",views.setting,name="setting"),
    path("terms_confitions,",views.terms_conditions,name="terms_conditions"),
    path("language/",views.language,name="language"),
    path("help/",views.help,name="help"),
    path("security/",views.security,name="security"),
]
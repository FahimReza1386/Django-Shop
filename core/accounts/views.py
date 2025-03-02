from django.shortcuts import render
from django.contrib.auth import views as auth_views
from accounts.forms import AuthenticationsForm
# Create your views here.

class UserLoginView(auth_views.LoginView):
    template_name="accounts/login.html"
    form_class=AuthenticationsForm
    redirect_authenticated_user=True



class UserLogoutView(auth_views.LogoutView):
    pass



class ResetPasswordView(auth_views.PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = '/'



class CustomPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name="accounts/password_reset_complete.html"
    success_url='/accounts/login/'


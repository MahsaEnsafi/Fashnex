from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, views as auth_views
from django.contrib import messages
from django.urls import reverse_lazy
from django.conf import settings
from django.contrib.auth.decorators import login_required

from account.forms import SignUpForm


# --------------------------------------------------
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Signup successful! You can now log in.')
            return redirect('accounts:login')
    else:
        form = SignUpForm()

    return render(request, 'account/signup.html', {'form': form})


# --------------------------------------------------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(request, username=username_or_email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('/')
        else:
            messages.error(request, 'Invalid username/email or password.')

    return render(request, 'account/login.html')


# --------------------------------------------------
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')


# --------------------------------------------------
class CustomPasswordResetView(auth_views.PasswordResetView):
    template_name = 'account/password_reset.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = 'account/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:login')
    from_email = settings.DEFAULT_FROM_EMAIL

    def form_valid(self, form):
        messages.success(
            self.request,
            "If an account with this email exists, a password reset link has been sent."
        )
        return super().form_valid(form)
#------------------------------------------------------------------------
class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = "account/password_reset_confirm.html"
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 
                         "Your password has been changed successfully. You can now log in.")
        return response

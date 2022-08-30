from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib import messages
from users.forms import UserSignUpForm, EmailMessageForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, 'users/index.html')

def signup(request):

    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            form.save()

   
            messages.success(request, f'Your account has been created')
            return redirect('login')
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def send_email(request):

    if request.method == 'POST':
        form = EmailMessageForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']

            message = form.cleaned_data['message']

            user_id = form.cleaned_data['user_id']

            user = User.objects.get(id=user_id)

            user.email_user(subject, message, request.user.get_full_name(),
                                                    fail_silently=True)
            
            messages.success(request, f'An email has been sent to {user.get_full_name()}')

            return redirect('index')
    else:
        form = EmailMessageForm()

    context = {
        'form': form,
    }
    return render(request, 'users/send_email.html', context)



# Create your views here.

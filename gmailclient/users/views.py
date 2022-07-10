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
    # do the following when a user, submits the form which sends/returns a POST request to the same view
    # and sends/returns with it the POST data submited in the form
    if request.method == 'POST':
        # instantiate a new form with the POST data submitted
        form = UserSignUpForm(request.POST)
        # check if the submitted form data is valid
        if form.is_valid():
            # call the form save method to save the data into the DB
            form.save()

            # the messages python module simply sends a message back to the HTML template 
            # rendering this view, for you to display to the user
            messages.success(request, f'Your account has been created')
            return redirect('login')
    # pass the blank sign up form when a user navigates to this page through a GET request
    else:
        form = UserSignUpForm()
    return render(request, 'users/signup.html', {'form': form})

# we will use the django built in method/decorator called @login_required
# to force a user to log in first before accessing this view/webpage
@login_required
def send_email(request):
    # do the following when a user, submits the form which sends/returns a POST request to the same view
    # and sends/returns with it the POST data submited in the form
    if request.method == 'POST':
        # instantiate a new form with the POST data submitted
        form = EmailMessageForm(request.POST)
        # check if the submitted form data is valid
        if form.is_valid():
            # get the submitted subject
            subject = form.cleaned_data['subject']

            # get the submitted message
            message = form.cleaned_data['message']

            # get the submitted user_id, which is the value of the option that was selected and submitted
            user_id = form.cleaned_data['user_id']

            # get the user associated with the passed user_id
            user = User.objects.get(id=user_id)

            # call the built in email_user method on the returned user object
            # enter the email subject, message and the name of whom the email is from
            # set it to fail silently if an error occurrs
            # this email will be sent to the users email inbox/spam folder
            user.email_user(subject, message, request.user.get_full_name(),
                                                    fail_silently=True)
            
            # All emails sent will be viewed on the configured Google Email Account in the settings.py file
            # Log into the Gmail account of the configured Google Email Account in the settings.py file
            # Navigate to the sent folders to view all emails sent and any error messages sent back

            # the messages python module simply sends a message back to the HTML template 
            # rendering this view, for you to display to the user
            messages.success(request, f'An email has been sent to {user.get_full_name()}')

            # redirect the user back to the home page
            return redirect('index')
    # pass the blank email message form when a user navigates to the email page through a GET request
    else:
        form = EmailMessageForm()

    context = {
        'form': form,
    }
    return render(request, 'users/send_email.html', context)



# Create your views here.

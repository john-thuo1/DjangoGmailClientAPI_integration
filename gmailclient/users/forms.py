from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.db.models import CharField, Value as V, F
from django.db.models.functions import Concat


class UserSignUpForm(UserCreationForm):
    '''
    We will instantiate the email field inside this form, so as to make it a mandatory field, 
    we will also set the form to interact with the model or database table called “User”, 
    while also stating that specific fields from the user table to be displayed on the form when displayed for user input.
    These fields are:
•	“first_name”: a field to enter a user’s first name
•	“last_name”: a field to enter a user’s last name
•	“username”: a field to enter a user’s username to be used during log ins
•	“email”: a field to enter a user’s email address
•	“password1”: a field to enter the new password for the user account to be created
•	“password2

    '''
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class EmailMessageForm(forms.Form):
    CHOICES = User.objects.all().values_list(   
                    # the data to be held in the value field of the dropdowns e.g. the HTML option tag
                    'id',
    
                    # the user friendly value that will be displayed to the user is the User Fullname
                    # which will be a concatination of the users' first_name and last_name
                    # I am placing the V(' ') between the names simply to create a space during concatination
                    Concat(
                            F('first_name'), V(' '), F('last_name'),

                            #how the data is to be outputted
                            output_field=CharField()
                        )
                )

    # the drop down to hold registered active users' (users not deleted/deactivated) fullnames and user database ids
    # the drop down is to be populated with data from the CHOICES variable above
    user_id = forms.ChoiceField(choices=CHOICES)

    # the email subject
    subject = forms.CharField(max_length=100)

    # the email message textarea
    message = forms.CharField(max_length=2000,widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(EmailMessageForm, self).__init__(*args, **kwargs) # Call to ModelForm constructor
        self.fields['subject'].widget.attrs['style'] = 'width:100%;'
        self.fields['message'].widget.attrs['cols'] = 150




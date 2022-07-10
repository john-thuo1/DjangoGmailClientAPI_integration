from django.urls import path, include


from django.contrib.auth import views as auth_views

from users.views import index, signup, send_email

urlpatterns = [
    # the name param in the path method is the name passed to the url tag inside the HTML template pages
    # e.g <a href=" {% url 'signup' %} "> This is an example of a link</a>
    # the url tag above will then resolve the name param to the appropriate http url
    # e.g http://127.0.0.1/signup   
    path('', index, name='index'),
    path('signup/', signup, name='signup'), 
    path('send_email/', send_email, name='send_email'), 

    # this url will use the builtin django log in view, but we have to pass a template
    # that the view will use to pass its authentication/log in form to for users to enter log in credentials
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),

    # we will utilise the builtin django views on the urls below
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    # a path to a page where you enter your email to request for a password reset
    path('passwod-reset/', auth_views.PasswordResetView.
         as_view(template_name="users/password_reset.html"),
         name='password_reset'),
    # the link to the page where you will reset your password, this link will be emailed to you
    # using the email settings provided in the projects settings.py file
    path('passwod-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.
         as_view(template_name="users/password_reset_confirm.html"),
         name='password_reset_confirm'),
    # a page to inform the user that an email with the link above has been successfully sent
    path('passwod-reset/done/', auth_views.PasswordResetDoneView.
         as_view(template_name="users/password_reset_done.html"),
         name='password_reset_done'),
    # the page a user will be redirected to once they reset their email from the emailed link above
    path('passwod-reset-complete', auth_views.PasswordResetCompleteView.
         as_view(template_name="users/password_reset_complete.html"),
         name='password_reset_complete'),
]
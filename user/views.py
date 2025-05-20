from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# request -> response
# request handler
# action 


from django.db import connections
from django.db.utils import OperationalError

#From Tutorial
from datetime import datetime
#Include for login functionalities
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView


#implement class based view
from django.views.generic import TemplateView

class LoginInterfacaeView(LoginView):
    template_name = "login.html"
    redirect_authenticated_user = "/share/"

class LogoutInterfacaeView(LogoutView):
    template_name = "logout.html"
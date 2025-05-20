from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, FileResponse

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

from django.views.generic import CreateView, DetailView, ListView, UpdateView, FormView

from .models import *
#from .forms import FileForm

#Don'tneed to reference the .py files to access the classes
from share.forms.fileform import FileForm
from share.forms.shareform import ShareRetrievalForm

#implement class based view
from django.views.generic import TemplateView

#New Class that inherits from template view
class HomeView(TemplateView):
    template_name = 'home.html'
    extra_context = {'today': datetime.today()}

#New Class that inherits from template view
class UploadFileView(LoginRequiredMixin, CreateView):
    model = File
    template_name = 'files_form.html'
    success_url = '/share/files/'
    extra_context = {'today': datetime.today()}
    form_class = FileForm

#New Class that inherits from template view
class UpdateFileView(LoginRequiredMixin, UpdateView):
    model = File
    template_name = 'files_form.html'
    success_url = '/share/files/'
    extra_context = {'today': datetime.today()}
    form_class = FileForm

class RetrieveFileView(FormView):
    template_name = 'files/retrieve.html'
    success_url = '/share/file/retrieve'
    extra_context = {'today': datetime.today()}
    form_class = ShareRetrievalForm

    def post(self, request, *args, **kwargs):
        contact = request.POST.get("addr")
        file = request.POST.get("fileid")
        passcode = request.POST.get("passcode")
        

        try:
            ao = Access.get_Object(file, passcode)
            fileobject = ao.get_FileObject()
            #accesses = Access.objects.filter(username=file).filter(passcode=passcode).first()
            self.extra_context["file"] = fileobject
            #convert file object to string.
            #filename = fileobject.get_FilePath()

            file = ao.get_File()
            if file:
                response = FileResponse(open(ao.get_File(), 'rb'), as_attachment=True)
            else:
                response = HttpResponseRedirect('/share/file/download')
            #ao.countAttempt()
            return response
        except AttributeError:
            # REturn object couldn't be found
            go = None
        

        #Get File that matches this search info
        # print("Valid form submission..{0}, {1} & {2}".format(contact, file, passcode))
        # print(accesses.fileobj.title)
        return HttpResponseRedirect(self.get_success_url())





#New Class that inherits from template view
class DownloadFileView(TemplateView):
    template_name = 'files/download.html'
    extra_context = {'today': datetime.today()}

#Need to be logged in to view
class FilesListView(LoginRequiredMixin, ListView):
    model = File
    context_object_name = 'files'
    template_name = 'files_list.html'
    #login_url = "/admin"
    #queryset =  File.objects.all()

    # Override Get query set method
    def get_queryset(self):
        files = self.request.user.files.all()
        for file in files:
            file.shares = file.get_ShareCount()

        return files

class FileDetailView(LoginRequiredMixin, DetailView):
    model = File
    context_object_name = 'file'
    template_name = 'files_detail.html'

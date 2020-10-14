from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView
from .models import File
from django.http import HttpResponse, JsonResponse, Http404
from django.db.models import Q
import urllib.request as urlreq
from urllib.parse import quote
import requests
from django.http import StreamingHttpResponse
from django.contrib.messages.views import SuccessMessageMixin


# a global variable to show the heirarichal structure of the files catagories
#Warning: do not modify or write to the variable at run time
catagories = {

    "Computer" : {
        
        "Java" : {
            'Java Lab' : "",
        },

        "Logic" : "",
        "Embedded" : "",
    },

    "Electrical" : {

        "Amplifier" : {

            "Past Pappers" : "",
            "TextBooks" : "",
        },

        "Antennas" : {
            
            "Past Pappers" : "",
            "TextBooks" : "",


        },
    },

    "Science" : {

        "Calculus" : {

            'Calculus 1' : "",
            'Calculus 2' : "",
            'Calculus 3' : "",
        },

        "Chemistry 1" : "", 
    },
}




class FileCreationView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = File
    fields= ['name', 'file', 'login_required_to_view', 'description']
    template_name = "files/upload.html"
    success_message = "uploaded successfully awaiting admin review"
    

    #overriding this method to attach the  
    #current logged in user to the file before submiting
    def form_valid(self, form):
        form.instance.student = self.request.user
        return super(CreateView, self).form_valid(form)

    def get_success_url(self):
        return redirect("/")
    



class FileListView(ListView):
    model = File
    template_name = 'frontend/main.html'
    context_object_name = "files"
    ordering=['-upload_date']
    paginate_by = 8


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "All Files"
        return context


class FileSingleCatagoryListView(ListView):
    model = File
    template_name = 'frontend/main.html'
    context_object_name = "files"
    ordering=['-upload_date']
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(
            catagory1=self.kwargs["catagory1"]
            )
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catagory1'] = self.kwargs["catagory1"]
        context['title'] = "Catagory : " + self.kwargs["catagory1"]
        return context


class FileDualCatagoryListView(ListView):
    model = File
    template_name = 'frontend/main.html'
    context_object_name = "files"
    ordering=['-upload_date']
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(
            catagory1=self.kwargs["catagory1"],
            catagory2=self.kwargs["catagory2"],
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catagory1'] = self.kwargs["catagory1"]
        context['catagory2'] = self.kwargs["catagory2"]
        context['title'] = f'Catagory: {self.kwargs["catagory1"]} > {self.kwargs["catagory2"]}'

        return context



class FileTripleCatagoryListView(ListView):
    model = File
    template_name = 'frontend/main.html'
    context_object_name = "files"
    ordering=['-upload_date']
    paginate_by = 8   

    def get_queryset(self):
        return super().get_queryset().filter(
            catagory1=self.kwargs["catagory1"],
            catagory2=self.kwargs["catagory2"],
            catagory3=self.kwargs["catagory3"],
            ) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['catagory1'] = self.kwargs["catagory1"]
        context['catagory2'] = self.kwargs["catagory2"]
        context['catagory3'] = self.kwargs["catagory3"]
        context['title'] = f'Catagory: {self.kwargs["catagory1"]} > {self.kwargs["catagory2"]} > {self.kwargs["catagory3"]}'

        return context





class FileSearchListView(ListView):
    model = File
    template_name = 'frontend/main.html'
    context_object_name = "files"
    ordering=['-upload_date']
    paginate_by = 8

    def get_queryset(self):
        return super().get_queryset().filter(
            Q(catagory1__icontains=self.kwargs["search_data"]) | 
            Q(catagory2__icontains=self.kwargs["search_data"]) | 
            Q(catagory3__icontains=self.kwargs["search_data"]) | 
            Q(name__icontains=self.kwargs["search_data"]) | 
            Q(description__icontains=self.kwargs["search_data"] ))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_data'] = self.kwargs["search_data"]
        context['title'] = f'Search results for: {self.kwargs["search_data"]}'

        return context





def download_file(request, file_id):

    obj = File.objects.get(pk=file_id)

    if obj:

        extension = obj.extension()
        
        content_type = obj.content_type()
        url = "https://zenonbank.blob.core.windows.net/media/" + quote(obj.file.name)

        """
        file = urlreq.urlopen(url).read()
        
        
        response = HttpResponse(file, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename={quote(obj.filename())}' 
        """

        r = requests.get(url, stream=True)

        resp = StreamingHttpResponse(streaming_content=r)
        resp['Content-Disposition'] = f'attachment; filename={quote(obj.filename())}'

        obj.download_count += 1
        obj.save()

        return resp


    raise Http404


def view_file_embedded(request, file_id):
    obj = File.objects.get(pk=file_id)

    if obj:

        extension = obj.extension()
        file = obj.file
        
        content_type = obj.content_type()
        with open(file.path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=content_type)
            response['Content-Disposition'] = f'inline; filename={quote(obj.filename())}' 
            f.close()
            return response


    raise Http404



def get_catagories(request):
    global catagories
    
    response = JsonResponse(data=catagories, safe=False)
    return response






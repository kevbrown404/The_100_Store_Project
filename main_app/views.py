from django.shortcuts import redirect, render
from django.views import View # <- View class to handle requests
from django.http import HttpResponse # <- a class to handle sending a type of response
#...
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView
from .models import Designer, Item
from django.urls import reverse

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



# Create your views here.

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["designers"] = Designer.objects.filter(name__icontains=name)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {name}"
        else:
            context["designers"] = Designer.objects.filter() # Here we are using the model to query the database for us.
                        # default header for not searching 
            context["header"] = "Trending designers"
        return context
    
class About(TemplateView):
    template_name = "about.html"
    
@method_decorator(login_required, name='dispatch')
class DesignerList(TemplateView):
    template_name = "designer_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["designers"] = Designer.objects.filter(name__icontains=name)
            # We add a header context that includes the search param
            context["header"] = f"Searching for {name}"
        else:
            context["designers"] = Designer.objects.filter() # Here we are using the model to query the database for us.
                        # default header for not searching 
            context["header"] = "Trending designers"
        return context
    
class DesignerCreate(CreateView):
    model = Designer
    fields = ['name', 'img', 'bio', 'verified_designer']
    template_name = "designer_create.html"
    success_url = "/designers/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(DesignerCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('designer_detail', kwargs={'pk': self.object.pk})


class DesignerDetail(DetailView):
    model = Designer
    template_name = "designer_detail.html"

class DesignerUpdate(UpdateView):
    model = Designer
    fields = ['name', 'img', 'bio', 'verified_designer']
    template_name = "designer_update.html"
    success_url = "/designers/"

    def get_success_url(self):
        return reverse('designer_detail', kwargs={'pk': self.object.pk})

class DesignerDelete(DeleteView):
    model = Designer
    template_name = "designer_delete_confirmation.html"
    success_url = "/designers/"

class ItemCreate(View):

    def post(self, request, pk):
        title = request.POST.get("title")
        length = request.POST.get("length")
        designer = Designer.objects.get(pk=pk)
        Item.objects.create(title=title, length=length, designer=designer)
        return redirect('designer_detail', pk=pk)
    
class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("designer_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)

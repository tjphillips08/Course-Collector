from django.shortcuts import render,redirect
from django.views import View # <- View class to handle requests
from django.urls import reverse
from django.http import HttpResponse # <- a class to handle sending a type of response
from django.views.generic.base import TemplateView
from .models import Course, Member, Club
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# after our other imports 
from django.views.generic import DetailView
# at top of file with other imports
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
        context=super().get_context_data(**kwargs)
        context["clubs"] = Club.objects.all()
        return context


class About(TemplateView):
    template_name = "about.html"

# random comment
# Create your views here.
 #adds artist class for mock database data
# class Course:
#     def __init__(self, name, image, address):
#         self.name = name
#         self.image = image
#         self.address = address


# courses = [
#   Course("The Course at Eagle Mountain", "https://i.imgur.com/wloXfgum.jpg",
#           "800 Gap Rd, Batesville, AR 72501"),
#   Course("Batesville Municipal Golf Course",
#           "https://i.imgur.com/Kd2QKoZm.jpg", "1850 Chaney Dr, Batesville, AR 72501"),
#   Course("Cooper's Hawk Golf Course", "https://i.imgur.com/hhoyzaSm.jpg",
#           "AR-69 Spur, Melbourne, AR 72556"),
 

@method_decorator(login_required, name='dispatch')
class CourseList(TemplateView):
    template_name = "course_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mySearchName = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if mySearchName != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["courses"] = Course.objects.filter(name__icontains=mySearchName, user=self.request.user)
            context["stuff_at_top"] = f"Searching through Courses list for {mySearchName}"
        else:
            context["courses"] = Course.objects.filter(user=self.request.user)
            context["stuff_at_top"] = "Trending Courses"
        return context


class CourseCreate(CreateView):
    model = Course
    fields = ['name', 'img', 'address', 'website']
    template_name = "course_create.html"
    
    # This is our new method that will add the user into our submitted form
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CourseCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('course_detail', kwargs={'pk': self.object.pk})
   



class CourseDetail(DetailView):
    model = Course
    template_name = "course_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["clubs"] = Club.objects.all()
        return context

class CourseUpdate(UpdateView):
    model = Course
    fields = ['name', 'img', 'address', 'website']
    template_name = "course_update.html"
    success_url = "/Courses/"

    def get_success_url(self):
        return reverse('Course_detail', kwargs={'pk': self.object.pk})

class CourseDelete(DeleteView):
    model = Course
    template_name = "course_delete_confirmation.html"
    success_url = "/courses/"

class MemberCreate(View):

    def post(self, request, pk):
        formName = request.POST.get("name")
        formLength = request.POST.get("length")
        formEmail = request.POST.get("email")
        theCourse = Course.objects.get(pk=pk)
        Member.objects.create(name=formName, length=formLength, email=formEmail,course=theCourse)
        return redirect('course_detail', pk=pk)



class ClubMemberAssoc(View):
    def get(self, request,pk, member_pk):
        if assoc == "remove":
            Club.objects.get(pk=pk).members.remove(member_pk)
        if assoc =="add":
            Club.objects.get(pk=pk).members.add(member_pk)
        return redirect('home')


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
            return redirect("course_list")
        else:
            context = {"form": form}
            return render(request, "registration/signup.html", context)

        
from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse_lazy , reverse
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from django.views.generic.edit import FormView , UpdateView , CreateView
from django.contrib.auth.decorators import login_required


from django.contrib.auth.mixins import UserPassesTestMixin , LoginRequiredMixin

from django.db.models import Q
from .models import HunterProfile , CompanyProfile , ProjectPost , Project
from .forms import AccountTypeForm , CreateProjectForm , CreatePostForm

# Create your views here.
def landing_page(request):
    return render(request , 'base/landing_page.html')

def home(request , slug=None):
    context = {}
    context['projects'] = None
    if slug:
        context['slug'] = slug
        search_query = request.GET.get("search" , "")
        if search_query:
            projects = Project.objects.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )
        elif not search_query:
            projects = Project.objects.filter(is_active = True)
        if projects.exists():
            context['projects'] = projects

        if slug.upper() == "HUNTER":
            profile = get_object_or_404(HunterProfile , user = request.user)
            context['profile'] = profile

            
        if slug.upper() == "COMPANY":
            profile = get_object_or_404(CompanyProfile , user = request.user)
            context['profile'] = profile
            
    
    return render(request , "base/home.html" , context)


            

class AccountType(UserPassesTestMixin , FormView ):
    form_class= AccountTypeForm
    success_url = reverse_lazy("home")
    template_name = "base/account_selection.html"


    def form_valid(self, form):
        account_type = form.cleaned_data['account_type']

        if account_type.upper() == "HUNTER" :
            profile,created = HunterProfile.objects.get_or_create(
                user= self.request.user,
            )
            self.slug = "hunter"

        elif account_type.upper() == "COMPANY":
            profile , created = CompanyProfile.objects.get_or_create(
                user= self.request.user,
            )
            self.slug="company"
        profile.save()


        return super().form_valid(form)
    
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        hunter_profile = HunterProfile.objects.filter(user = self.request.user)
        company_profile = CompanyProfile.objects.filter(user = self.request.user)
        if hunter_profile.exists() or company_profile.exists() :
            if hunter_profile.exists():
                self.slug = "hunter"
            elif company_profile.exists():
                self.slug = "company"
            return False
        else:
            return True

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse("home" , kwargs={"slug":self.slug}))
    
    def get_success_url(self):
        return reverse("profile_check" , kwargs={"slug":self.slug})

def profile_checker(request , slug):
    if slug.upper()=="HUNTER":
        profile = get_object_or_404(HunterProfile , user=request.user)
        return redirect(reverse("edit_hunter_profile" , kwargs={"pk": profile.id}))
    elif slug.upper()=="COMPANY":
        profile = get_object_or_404(CompanyProfile , user=request.user)
        return redirect(reverse("edit_company_profile" , kwargs={"pk": profile.id}))
        
class EditHunterProfile(UpdateView):
    model = HunterProfile
    fields=["name" , "description" , "education"]
    template_name="base/edit_profile.html"
    success_url = reverse_lazy("hunter_profile")

@login_required
def hunter_profile(request):
    try:
        profile = get_object_or_404(HunterProfile , user= request.user)
    except Http404 :
        return redirect(reverse_lazy("account_selection"))
    
    context={
        "profile":profile
    }
    return render(request , "base/hunter_profile.html" , context)

class CreatePost(FormView , LoginRequiredMixin):
    form_class = CreatePostForm
    template_name = "base/create_post.html"
    

    def form_valid(self, form):
        hunter_profile = get_object_or_404(HunterProfile , user = self.request.user)
        project = get_object_or_404(Project , id = self.kwargs.get("project_id"))
        post = form.save(commit=False)
        post.poster = hunter_profile
        post.project = project
        post.save()
        self.post_id = post.id
        self.project_id = project.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_page" , kwargs={"project_id": self.project_id})


#COMPANY VIEWS
    
class EditCompanyProfile(UpdateView):
    model = CompanyProfile
    fields=["name" ,"industry" , "description"]
    template_name="base/edit_profile.html"
    success_url = reverse_lazy("company_profile")
    
def company_profile(request):
    profile = get_object_or_404(CompanyProfile , user= request.user)
    context={
        "profile":profile
    }
    return render(request , "base/company_profile.html" , context)


class CreateProject(FormView , LoginRequiredMixin):
    form_class = CreateProjectForm
    template_name = "base/create_project.html"
    

    def form_valid(self, form):
        company_profile = get_object_or_404(CompanyProfile , user = self.request.user)
        project = form.save(commit=False)
        project.company = company_profile
        project.save()
        self.project_id = project.id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("project_page" , kwargs={"project_id": self.project_id})
    

def project_page(request , project_id):
    hunter_profile = HunterProfile.objects.filter(user = request.user)
    company_profile = CompanyProfile.objects.filter(user= request.user)
    project = get_object_or_404(Project , id=project_id)
    project_posts = ProjectPost.objects.filter(project=project).order_by("-created")
    context={
        "project":project,
        "posts": project_posts
    }
    if hunter_profile.exists():
        context['slug'] = "hunter"
    elif company_profile.exists():
        context['slug'] = "company"
    else:
        return Http404
    print(context["slug"])
    return render(request , "base/project_page.html" , context)

def project_post_page(request , project_id , post_id):
    project = get_object_or_404(Project , id=project_id)
    post = get_object_or_404(ProjectPost , id=post_id)
    context ={
        "post": post,
        "project": project
    }
    return render(request , "base/post_detail.html" , context)

def bug_dashboard(request):
    company_profile = get_object_or_404(CompanyProfile , user=request.user)
    bugs = ProjectPost.objects.filter(
    Q(project__company=company_profile) & Q(post_type=ProjectPost.Post_Type.BUG)
).order_by('-created')

    context = {
        "bugs": bugs
    }

    return render(request , "base/bug_dashboard.html" , context)
    
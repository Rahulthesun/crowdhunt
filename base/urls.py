from django.urls import path 
from . import views
from users import views as user_views
from users.views import EmailLogin , EmailSignup
from .views import AccountType ,EditHunterProfile , EditCompanyProfile , CreateProject , CreatePost
from django.contrib.auth.views import LogoutView 

urlpatterns = [
    path("", views.landing_page , name="landing_hunter" ),
    path("home/<slug:slug>/", views.home , name="home" ),
    path("login/", EmailLogin.as_view(next_page="") , name="login" ),
    path("signup/", EmailSignup.as_view() , name="signup" ),
    path("profile_checker/<slug:slug>/" ,views.profile_checker , name="profile_check" ),
    path("logout/" , LogoutView.as_view(next_page="login") , name="logout" ),


    path("account_selection/" , AccountType.as_view() , name="account_selection"),
    path("edit_profile/hunter/<str:pk>/" , EditHunterProfile.as_view() , name="edit_hunter_profile"),
   
    path("view_profile/hunter/" , views.hunter_profile , name="hunter_profile"),
    path("create_post/project/company/<int:project_id>/" , CreatePost.as_view() , name="create_post"),
    path("view_post/project/<int:project_id>/<int:post_id>" , views.project_post_page , name="view_post"),
    


    #company_urls
    path("edit_profile/company/<str:pk>/" , EditCompanyProfile.as_view() , name="edit_company_profile"),
    path("view_profile/company/" , views.company_profile , name="company_profile"),
    path("create_project/company/" , CreateProject.as_view() , name="create_project"),
    path("view_project/<int:project_id>" , views.project_page , name="project_page"),
    path("bug_dashboard/company/" , views.bug_dashboard , name="bug_dashboard"),


]
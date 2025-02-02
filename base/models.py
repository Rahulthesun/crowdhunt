from django.db import models
from users.models import EmailUser
from django.core.validators import MinValueValidator

# Create your models here.

class HunterProfile(models.Model):
    user=models.OneToOneField(EmailUser , on_delete=models.SET_NULL , null=True)
    name=models.CharField(max_length=200 , null=False , blank=False)
    description=models.TextField(null=True , blank=True)
    education=models.TextField(null=True , blank=True)
    #rating =
    bugs_found = models.IntegerField(default=0 , validators=[MinValueValidator(0)])
    rewards_earned = models.DecimalField(max_digits=10 , decimal_places=2, default=0.00 , validators=[MinValueValidator(0)])

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name and self.user.email:
            return f"{self.name}--{self.user.email}"
        else:
            return "Unrecognized HunterProfile"
        
class CompanyProfile(models.Model):
    user = models.OneToOneField(EmailUser , on_delete=models.SET_NULL , null=True)
    name=models.CharField(max_length=200 , null=False , blank=False)
    industry=models.CharField(max_length=200 , null=False , blank=False)
    description=models.TextField(null=True , blank=True)
    website = models.URLField(null=True , blank=True)
    projects_hosted = models.IntegerField(default=0 , validators=[MinValueValidator(0)])
    
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name and self.user.email:
            return f"{self.name}--{self.user.email}"
        else:
            return "Unrecognized CompanyProfile"
    

class Project(models.Model):
    company = models.ForeignKey(CompanyProfile , on_delete=models.SET_NULL , null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=False , blank=False)
    #rewards.
    website = models.URLField(null=True , blank=True)
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class ProjectPost(models.Model):
    poster = models.ForeignKey(HunterProfile , on_delete=models.SET_NULL , null=True)
    project = models.ForeignKey(Project , on_delete=models.SET_NULL , null=True)
    text = models.TextField(null=False , blank=False)

    #picture

    class Post_Type(models.TextChoices):
        DISCUSSION = "DISCUSSION"
        BUG = "BUG"
    
    post_type = models.CharField(max_length=60 , choices=Post_Type.choices , default=Post_Type.DISCUSSION)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.poster.name}--{self.project.name} "
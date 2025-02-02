from django.contrib import admin
from .models import CompanyProfile , HunterProfile , Project , ProjectPost
# Register your models here.

admin.site.register(HunterProfile)
admin.site.register(CompanyProfile)
admin.site.register(Project)
admin.site.register(ProjectPost)



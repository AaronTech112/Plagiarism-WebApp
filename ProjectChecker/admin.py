from django.contrib import admin
from . models import CustomUser, Department, Project

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Department)
admin.site.register(Project)

from django.contrib import admin
from .models import Cerrajero, Rating, Ciudad, Available, Job

# Register your models here.

admin.site.register(Cerrajero)
admin.site.register(Rating)
admin.site.register(Ciudad)
admin.site.register(Available)
admin.site.register(Job)

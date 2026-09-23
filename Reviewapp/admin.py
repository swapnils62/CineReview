from django.contrib import admin
from .models import Review
# Register your models here.

@admin.register(Review)
class Adminmodel(admin.ModelAdmin):
    list_display=['Title','Review','Rating','Created_at','user','Movie']
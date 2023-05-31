from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','description','content','owner','is_public']

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['id','post','user']
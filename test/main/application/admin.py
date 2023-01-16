from django.contrib import admin

# Register your models here.

from .models import Post

class Postadmin(admin.ModelAdmin):
    list_display = ('title','created_on')

admin.site.register(Post,Postadmin)
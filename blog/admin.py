from django.contrib import admin
from .models import UpdatePost, Advertisement,Comment, Profile
# Register your models here.

admin.site.register(Advertisement)
admin.site.register(UpdatePost)
admin.site.register(Comment)
admin.site.register(Profile)

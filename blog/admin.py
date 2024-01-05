from django.contrib import admin
from .models import UpdatePost, Advertisement,Comment, Profile,DailyTask
# Register your models here.

admin.site.register(Advertisement)
admin.site.register(UpdatePost)
admin.site.register(Comment)
admin.site.register(Profile)
admin.site.register(DailyTask)

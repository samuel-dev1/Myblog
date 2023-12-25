from django.db import models

# Create your models here.

from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
import random
import string

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default='default.png', upload_to="profile_pic")
    slug = models.SlugField(blank=False, null=False, unique=True)
    def __str__(self) -> str:
        return str(self.user.username)+(" profile")
    def get_absolute_url(self):
        return reverse("details", kwargs={"slug": self.slug})
@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        t = "".join(random.choice(string.ascii_lowercase+string.digits)
                    for x in range(15))
        t_to_str = str(t)
        Profile.objects.create(user=instance, slug=t_to_str)
    instance.profile.save()
class UpdatePost(models.Model):
    category = (
        (
        "News","News"
        ),
          (
        "Education","Education"
        ),
        ('Politics',"Politics"),
        ("Sport","Sport"),
        ("Entertainmnt","Entertaiment" )
        )
    title = models.CharField(max_length= 150)
    image =  models.ImageField(blank= False, upload_to = "Media")
    catgories =  models.CharField(choices = category, default = "News" ,max_length=100)
    discriptions =RichTextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=200, unique= True)
    def __str__(self) -> str:
        return str(self.title)
class Advertisement(models.Model):
    image =  models.ImageField(blank= False, upload_to = "Advert")
    title = models.CharField(max_length =150)
    date_posted =models.DateTimeField(auto_now_add=True)
    def __str__ (self):
        return  str(self.title)

class Comment(models.Model):
    CommentPost = models.ForeignKey(
        UpdatePost, on_delete=models.CASCADE, related_name="comment")
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="author")
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-date_posted']
    def __str__(self):
        return str(self.author) + ' coment'






from django.urls import path
from .views import BlogHome, Entertaiment, Sport, Politics, Education, SearchMethod
from .views import details_view, Comments, loginPage, signup, log_out, activate, password_reset_request
urlpatterns = [
      path('login/', loginPage, name="login"),
    path('logout/', log_out, name="logout"),
    path('activate/<uidb64>/<token>/', activate, name="activate"),
    path('signup/', signup, name="signup"),
    path('',BlogHome, name="blog"),
    path('entertaiment/<str:element>',Entertaiment, name="Entertaiment"),
    path('sport/<str:element>',Sport, name="Sport"),
      path('politics/<str:element>',Politics, name="Politics"),
        path('education/<str:element>',Education, name="Education"),
        path('search',SearchMethod, name="search" ),
        path("read/<slug:slug>", details_view, name="readmore"),
        path("comment",Comments, name="comment"),
]
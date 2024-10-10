from django.urls import path
from .views import BlogHomeAPI,Movies, SearchDb, CommentAPI,AdvertismentAPI,PostFieldViewSetR

urlpatterns = [
    path('api/bloghome/', BlogHomeAPI.as_view(), name='blog-home-api'),
    path('api/advert/', AdvertismentAPI.as_view(), name='advert'),
    path("api/Movies",Movies.as_view(), name="movies"),
    path("api/seachDb",SearchDb.as_view(),name="seach"),
    path('api/comments/', CommentAPI.as_view(), name='comments-api'),
    path("api/details/<int:id>",PostFieldViewSetR.as_view())
]
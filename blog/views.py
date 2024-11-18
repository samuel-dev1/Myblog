from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator, PageNotAnInteger,EmptyPage
from .models import UpdatePost, Advertisement, Comment
from .serializers import UpdatePostSerializer, AdvertisementSerializer, CommentSerializer, DailyTaskSerializer, ProfileSerializer
from rest_framework.generics import RetrieveAPIView
import requests
import json
from bs4 import BeautifulSoup

class BlogHomeAPI(generics.ListAPIView):
    serializer_class = UpdatePostSerializer

    def get(self, request, *args, **kwargs):
        # Fetch all posts and filter by category if needed
        queryset = UpdatePost.objects.all().order_by("-date_posted")
        search_query = request.GET.get('params')
        print(search_query)
        if search_query:
            queryset = queryset.filter(catgories=search_query)
        paginator = Paginator(queryset, 10)  # 10 posts per page
        page_number = request.GET.get("page")
        
        try:
            paginated_data = paginator.page(page_number)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)

        # Get advertisement data
        advert = Advertisement.objects.all()

        # Prepare the banner; customize as per your logic
        postbanner = UpdatePost.objects.filter(catgories="News").first() if not search_query else None

        # Serialize the paginated data
        serializer = self.get_serializer(paginated_data, many=True)
        return Response({
            'posts': serializer.data,
            'postbanner': UpdatePostSerializer(postbanner).data if postbanner else None,
            'advert': AdvertisementSerializer(advert, many=True).data,
        })


class PostFieldViewSetR(RetrieveAPIView):
    queryset =UpdatePost.objects.all()
    serializer_class = UpdatePostSerializer
    lookup_field = 'id'
    
    
class CommentAPI(generics.CreateAPIView):
    serializer_class = CommentSerializer
    
    def get(self, request, *args, **kwargs):
        queryset =Comment.objects.all()
        post_id = self.request.GET.get("post_id")

        advert =Comment.objects.filter(CommentPost =post_id)

        return Response({
            'advert': CommentSerializer(advert, many=True).data,
        })
    
    def post(self, request, *args, **kwargs):
        comment = request.data.get("comment")
        post_id = request.data.get("id")
        if comment:
            new_comment = Comment.objects.create(
                CommentPost_id=post_id,
                content=comment,
                author=request.user,
            )
            return Response(CommentSerializer(new_comment).data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Comment cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)


class AdvertismentAPI(generics.ListAPIView):
    queryset = UpdatePost.objects.all().order_by("-date_posted")
    serializer_class = Advertisement

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()


        advert = Advertisement.objects.all()

        return Response({
            'advert': AdvertisementSerializer(advert, many=True).data,
        })
        
class SearchDb (generics.ListAPIView):
    queryset = UpdatePost.objects.all().order_by("-date_posted")
    serializer_class = UpdatePostSerializer
    
    def get(self, request, *kwargs, **args):
        search_p = self.request.data.get("search")
        if search_p:
            data = UpdatePost.objects(catgories=search_p)
            return Response({"data":data})
        return Response({data:None})
    

class Movies(generics.ListAPIView):
    def get(self, request, *kwargs, **args):
        url = "https://www.fzmovies.ng/"
        data = []
        response = requests.get(url)
        if response.status_code == 200:
            soap = BeautifulSoup(response.text, 'html.parser')
            find_text = soap.find_all("div",class_="post-filter-inside-wrap")
           
            for item in find_text:
                link1 = item.find("a")['href']
                image = item.find('img')['src']
                title = item.find('img')['alt']
                title_c = str(title)
                title_c.replace("Download"," ")
                entry_data = {
                    "link": link1,
                    "image": image,
                    "title":title_c,
                }
                data.append(entry_data)

        url = "https://www.awafim.tv/"
        response = requests.get(url)

        if response.status_code == 200:
            soap = BeautifulSoup(response.text, 'html.parser')
            
            # Find all movie entries
            find_movie = soap.find_all("a", class_="lu-one")
            
            for item in find_movie:
                # Extracting the link, image, and title
                link1 = item['href']  # No need to call item("a") since 'item' is already the anchor tag
                image = item.find('img')['src']
                title = item.find('h3').text
                # Clean the title (optional)
                title_c = title.replace("Download", "").strip()  # Removed "Download" and trimmed spaces
                # Print the results
                print("Link:", link1)
                print("Image:", image)
                print("Title:", title_c)
                # If you want to store the data
                entry_data = {
                    "link": link1,
                    "image": image,
                    "title": title_c,
                }
                data.append(entry_data)
    
            return Response({'data': data})
        else:
            return Response({'error_message': 'Failed to fetch data Error'})




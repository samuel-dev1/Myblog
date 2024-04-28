from django.shortcuts import render, HttpResponse, redirect, get_list_or_404, get_object_or_404
from .models import UpdatePost, Advertisement, Comment, DailyTask, Profile, MoviesAndMusic
from django.db.models.query_utils import Q
from .forms import SignUpForm, loginform, UpdateForm
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .tokens import account_activation_token
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from bs4 import BeautifulSoup
import requests
import json


def BlogHome(request):
    try:
        posts = UpdatePost.objects.all().order_by("-date_posted")
        paginator = Paginator(posts, 10)
        page = request.GET.get("page")
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)
        postbanner = UpdatePost.objects.get(id=1)
        advert = Advertisement.objects.all()
        context = {'posts': paginated_data,
                   'postbanner': postbanner, "advert": advert}
    except:
        context = {"null": None}
    return render(request, "index.html", context)

def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "templates/paswords/password_reset_email.txt/"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string("paswords/email_template.html", c)
                    try:
                        send_mail(subject, email, 'jsajosef@outlook.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="paswords/password_reset.html", context={"password_reset_form": password_reset_form})


def log_out(request):
    # loging out all the request from django log_out
    logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect("login")
    else:
        return HttpResponse('Activation link is invalid!')

def loginPage(request):
    """
     for login in user -> django auth+ usercreateform
    """
    f = loginform()  
    if request.method == "POST":
        username = request.POST.get("username")
        convername = username.lower()
        password = request.POST.get("password")
        user = authenticate(request, username=convername, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "login successful")
                return redirect('blog')
            else:
                messages.error(
                    request, "login error? check details or try forget password")
        else:
            messages.error(request, "Username does exits?")
    else:
        None
    return render(request, "authpage/login.html", {"f": f})
def signup(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile created continue")
            return redirect('login')
        else:
            messages.error(
                request, "Registration failed! kindly check your details")
    else:
        form = SignUpForm()
    return render(request, "authpage/signup.html", {"form": form})


def SearchMethod(request):
    try:
        if request.method == "POST":
            return HttpResponse("Invalid search pattern")
        else:
            searchtext = request.GET.get("seachpanel")
            if searchtext is not None:
                posts = UpdatePost.objects.all().order_by("-date_posted")
                advert = Advertisement.objects.all()
                product = UpdatePost.objects.filter(
                    Q(title__icontains=searchtext) or Q(catgories_icontains=searchtext))
                return render(request, 'pages/index.html', {"product": product, 'posts': posts, "advert": advert})
            else:
                return HttpResponse("Invalid search pattern")
    except:
        return HttpResponse("something went wrong")


def Entertaiment(request, element):
    try:
        posts = UpdatePost.objects.all().order_by("-date_posted")
        elements = UpdatePost.objects.filter(catgories=element).order_by("-date_posted")
        paginator = Paginator(elements, 15)
        page = request.GET.get('page')
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(paginator.num_pages)
        advert = Advertisement.objects.all()
        return render(request, "pages/full-width.html", {"post": paginated_data, 'posts': posts, "elements": element, "advert": advert})
    except:
        return HttpResponse("seomething went wrong!")


def Politics(request, element):
    try:
        posts = UpdatePost.objects.all().order_by("-date_posted")

        elements = UpdatePost.objects.filter(catgories=element).order_by("-date_posted")
        paginator = Paginator(elements, 15)
        page = request.GET.get('page')
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(paginator.num_pages)
        advert = Advertisement.objects.all()
        return render(request, "pages/full-width.html", {"post": paginated_data, 'posts': posts, "elements": element, "advert": advert})
    except:
        return HttpResponse("seomething went wrong!")


def Sport(request, element):

    try:
        posts = UpdatePost.objects.all().order_by("-date_posted")

        elements = UpdatePost.objects.filter(catgories=element).order_by("-date_posted")
        paginator = Paginator(elements, 15)
        page = request.GET.get('page')
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(paginator.num_pages)
        advert = Advertisement.objects.all()
        return render(request, "pages/full-width.html", {"post": paginated_data, 'posts': posts, "elements": element, "advert": advert})
    except:
        return HttpResponse("seomething went wrong!")


def Education(request, element):
    try:
        posts = UpdatePost.objects.all().order_by("-date_posted")

        elements = UpdatePost.objects.filter(catgories=element).order_by('-date_posted')
        paginator = Paginator(elements, 15)
        page = request.GET.get('page')
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(paginator.num_pages)
        advert = Advertisement.objects.all()
        return render(request, "pages/full-width.html", {"post": paginated_data, 'posts': posts, "elements": element, "advert": advert})
    except:
        return HttpResponse("seomething went wrong!")


def details_view(request, slug):
    obj = get_object_or_404(UpdatePost, slug=slug)
    obj3 = UpdatePost.objects.last()
    advert = Advertisement.objects.all()
    obj4 = UpdatePost.objects.filter(
        catgories=obj.catgories).order_by('-date_posted')
    coment = Comment.objects.filter(CommentPost_id=obj.id)
    return render(request, "pages/style-demo.html", {"object": obj, "object1": obj3, 'object2': obj4, "advert": advert, "comment": coment})


def Comments(request):
    if request.method == "POST":
        comment = request.POST.get("comment")

        submit_btt = request.POST.get("submit")
        if comment:
            obj = Comment.objects.get_or_create(
                CommentPost_id=submit_btt,
                content=comment,
                author=request.user,
            )
            return HttpResponse("working")
        else:
            return HttpResponse("does working")

def Movies(request):
    url = "https://www.fzmovies.ng/"
    response = requests.get(url)
    if response.status_code == 200:
        soap = BeautifulSoup(response.text, 'html.parser')
        find_text = soap.find_all("div",class_="post-filter-inside-wrap")
        data = []
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
        paginator = Paginator(data, 6)
        page = request.GET.get('page')
        try:
            paginated_data = paginator.page(page)
        except PageNotAnInteger:
            paginated_data = paginator.page(1)
        except EmptyPage:
            paginated_data = paginator.page(paginator.num_pages)
        return render(request, "pages/medias/movies.html", {'data': paginated_data})
    else:
        return render(request, "pages/error.html", {'error_message': 'Failed to fetch data Error'})
def Music(request):
    return render(request, "pages/error.html",{'error_message': 'Status="500"'})
@login_required
def NewsCaster(request):
    dailytask = DailyTask.objects.all()
    alltask = UpdatePost.objects.filter(user= request.user)
    profile =  Profile.objects.get(user= request.user)
    return render(request, "pages/employee/employee.html",{"daily":dailytask,"profile":profile,"post":alltask})

@login_required
def Create(request):
    form = UpdateForm()
    if request.method =="POST":
        form =UpdateForm(request.POST, request.FILES) 
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("home")
    else:
        form = UpdateForm()
    return render (request,"pages/form/upload.html",{"form":form} )


def Read(request):
    req = request.GET.get('home')  
    y = requests.get(req).text
    soup = BeautifulSoup(y, 'html.parser')
    find_p = soup.find("iframe", class_="BLOG_video_class")['src']
    image = soup.find('div', class_='post-body').find('a')['href']
    download_link = soup.find('div', class_='post-body').find('a', rel='nofollow', target='_blank')['href']
    return render(request, "pages/medias/contine.html" , {"find_p": find_p, "image": image, "download": download_link})





from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone

from myapp.forms import LoginForm, PostForm
from .models import Post


def readme(request):
    return render(request, 'myapp/readme.html', {})


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_list')
        else:
            print(form.is_valid())
    else:
        form = PostForm()
    return render(request, 'myapp/add_post.html', {
        'form': form
    })

@login_required
def post_list(request):
    if request.user.is_authenticated:
        login = request.user.id
        title_tables = ["Author", "Distance, m", "Duration, min", "Published date"]
        posts = Post.objects.filter(published_date__lte=timezone.now(), author=login).order_by('published_date')
        return render(request, 'myapp/post_list.html', {"posts": posts, "title_tables": title_tables})
    else:
        return HttpResponseRedirect('/login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            if form.get_user():
                login(request, form.get_user())
                return HttpResponseRedirect('/')
    else:
        form = LoginForm()
    return render(request, 'myapp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# @login_required
# def add_post(request):
#     if request.user.is_authenticated:
#         return render(request, 'myapp/add_post.html', {})
#     else:
#         return HttpResponseRedirect('/login')

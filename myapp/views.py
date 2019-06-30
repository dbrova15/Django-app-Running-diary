from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django_tables2 import RequestConfig

from myapp.forms import LoginForm, PostForm
from myapp.tables import PersonTable
from .models import Post


def readme(request):
    return render(request, 'myapp/readme.html', {})


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.speed = int(request.POST['distance'][0]) / int(request.POST['duration'][0])
            print(post)
            post.save()
            return redirect('post_list') #, pk=post.pk)
        else:
            print(form.is_valid())
    else:
        form = PostForm()
    return render(request, 'myapp/add_post.html', {
        'form': form
    })

@login_required
def post_list(request):  # todo фильтрация данных
    if request.user.is_authenticated:
        # if request.method == 'POST':
        #     login = request.user.id
        #     title_tables = ["Author", "Distance, m", "Duration, min", "Speed", "Published date"]
        #     table = PersonTable(
        #         Post.objects.filter(published_date__lte=timezone.now(), author=login, published_date__range=(start_date, end_date)).order_by('published_date'))
        #     RequestConfig(request).configure(table)

        login = request.user.id
        title_tables = ["Author", "Distance, m", "Duration, min", "Speed", "Published date"]
        table = PersonTable(Post.objects.filter(published_date__lte=timezone.now(), author=login).order_by('published_date'))
        RequestConfig(request).configure(table)
        return render(request, 'myapp/post_list.html', {"posts": table, "title_tables": title_tables})
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

@login_required
def del_post(request, id_post):
    post = get_object_or_404(Post, pk=id_post)
    query = post.delete()
    return redirect("/post_list", request, query)

@login_required
def edit_post(request, id_post):
    post = get_object_or_404(Post, pk=id_post)
    if request.method == "POST":
        form = PostForm(request.POST)
        print(request.POST)
        if form.is_valid():
            post.author = request.user
            post.speed = int(request.POST['distance'][0]) / int(request.POST['duration'][0])
            print(post)
            post.save()
            return redirect('post_list')  # , pk=post.pk)
        else:
            print(form.is_valid())
    else:
        form = PostForm(instance=post)
    return render(request, 'myapp/add_post.html', {
        'form': form
    })

@login_required
def statistic(request):
    return None
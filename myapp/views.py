import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, F, Count, Sum
from django.db.models.functions import ExtractWeek
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django_tables2 import RequestConfig

from myapp.forms import LoginForm, PostForm, ReportFiltersForm
from myapp.tables import PersonTable, StatTable
from .models import Post


def readme(request):
    return render(request, 'myapp/readme.html', {})


@login_required
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        # print(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.speed = round(int(request.POST['distance']) / int(request.POST['duration']) * 60 / 1000, 3)
            # print(post)
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
    # today = datetime.datetime.now()
    # last_year = today.year - 1
    # data_set = Post.objects.annotate(week=ExtractWeek('published_date')).values('week')
    # print(data_set)
    if request.user.is_authenticated:
        login = request.user.id
        table = PersonTable(
            Post.objects.filter(author=login))

        if table.rows.__len__() != 0:
            all_speed = [i.speed for i in Post.objects.filter(author=login)]
            average_speed = sum(all_speed) / len(all_speed)
        else:
            average_speed = 0
        if request.method == 'POST':
            form = ReportFiltersForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date'] + datetime.timedelta(days=1)
                table = PersonTable(
                    Post.objects.filter(author=login, published_date__range=(start_date, end_date)))
        else:
            form = ReportFiltersForm()

        title_tables = ["Author", "Distance, m", "Duration, min", "Speed", "Published date"]
        RequestConfig(request).configure(table)
        return render(request, 'myapp/post_list.html', {"posts": table, "title_tables": title_tables, 'form': form, 'average_speed': average_speed})
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
        if form.is_valid():
            post.author = request.user
            # post.speed = int(request.POST['distance'][0]) / int(request.POST['duration'][0]) * 60
            post.speed = round(int(request.POST['distance']) / int(request.POST['duration']) * 60 / 1000, 3)
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
    # today = datetime.datetime.now()
    month_12 = (datetime.datetime.today() - datetime.timedelta(days=30) * 12).month
    last_year = datetime.datetime.now().year - 1
    login = request.user.id

    data_set = Post.objects.filter(author=login, published_date__year__gte=last_year).annotate(
        week=ExtractWeek('published_date')
    ).values('week').annotate(
        all_records=Count('speed')
    ).annotate(
        sum_distance=Sum('distance')
    ).annotate(
        total_duration=Sum('duration')
    ).annotate(
        average_speed=Avg(F('speed'))
    ).order_by('week')
    print(data_set)
    table = StatTable(data_set)
    RequestConfig(request).configure(table)
    return render(request, 'myapp/stat.html', {"table": table})
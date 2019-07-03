import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, F, Count, Sum
from django.db.models.functions import ExtractWeek
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django_tables2 import RequestConfig

from myapp.forms import LoginForm, PostForm, ReportFiltersForm
from myapp.tables import PersonTable, StatTable
from .models import Post


def readme(request):
    return render(request, 'myapp/readme.html', {})


@login_required
def add_data(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.speed = round(int(request.POST['distance']) / int(request.POST['duration']) * 60 / 1000, 3)
            post.save()
            return redirect('data_list')
        else:
            print(form.is_valid())
    else:
        form = PostForm()
    return render(request, 'myapp/add_data.html', {
        'form': form
    })


def default_table(login):
    list_data = Post.objects.filter(author=login)
    table = PersonTable(list_data)

    if table.rows.__len__() != 0:
        all_speed = [i.speed for i in list_data]
        average_speed = sum(all_speed) / len(all_speed)
    else:
        average_speed = 0
    return table, average_speed


@login_required
def data_list(request):
    if request.user.is_authenticated:
        login = request.user.id

        if request.method == 'POST':
            form = ReportFiltersForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date'] - datetime.timedelta(days=1)
                end_date = form.cleaned_data['end_date'] + datetime.timedelta(days=1)
                list_data = Post.objects.filter(author=login, published_date__range=(start_date, end_date))
                table = PersonTable(list_data)
                if table.rows.__len__() != 0:
                    all_speed = [i.speed for i in list_data]
                    average_speed = sum(all_speed) / len(all_speed)
                else:
                    average_speed = 0
            else:
                table, average_speed = default_table(login)
        else:
            table, average_speed = default_table(login)

        form = ReportFiltersForm()

        title_tables = ["Author", "Distance, m", "Duration, min", "Speed", "Published date"]
        RequestConfig(request).configure(table)
        return render(request, 'myapp/data_list.html',
                      {"posts": table, "title_tables": title_tables, 'form': form, 'average_speed': average_speed})
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
def del_data(request, id_post):
    post = get_object_or_404(Post, pk=id_post)
    query = post.delete()
    return redirect("/data_list", request, query)


@login_required
def edit_data(request, id_post):
    post = get_object_or_404(Post, pk=id_post)
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post.author = request.user
            # post.speed = int(request.POST['distance'][0]) / int(request.POST['duration'][0]) * 60
            post.speed = round(int(request.POST['distance']) / int(request.POST['duration']) * 60 / 1000, 3)
            post.save()
            return redirect('data_list')
        else:
            print(form.is_valid())
    else:
        form = PostForm(instance=post)
    return render(request, 'myapp/add_data.html', {
        'form': form
    })


@login_required
def statistic(request):
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

    table = StatTable(data_set)
    RequestConfig(request).configure(table)
    return render(request, 'myapp/stat.html', {"table": table})

import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Avg, F, Count, Sum
from django.db.models.functions import ExtractWeek
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from django_tables2 import RequestConfig

from myapp.forms import PostForm, ReportFiltersForm
from myapp.tables import PersonTable, StatTable
from .models import Add_data


def get_speed(distance, duration):
    try:
        speed = round(int(distance) / int(duration) * 60 / 1000, 3)
    except ZeroDivisionError:
        return 0
    return speed


def readme(request):
    return render(request, 'myapp/readme.html', {})


@login_required
def add_data(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.speed = get_speed(request.POST['distance'], request.POST['duration'])
            post.save()
            return redirect('data_list')
        else:
            print(form.is_valid())
    else:
        form = PostForm()
    return render(request, 'myapp/add_data.html', {
        'form': form
    })


def get_average_speed(list_data):
    if len(list_data) != 0:
        all_speed = [i.speed for i in list_data]
        average_speed = sum(all_speed) / len(all_speed)
    else:
        average_speed = 0
    return average_speed


def user_data_table(login):
    list_data = Add_data.objects.filter(author=login)
    table = PersonTable(list_data)

    return table, get_average_speed(list_data)


@login_required
def data_list(request):
    if request.user.is_authenticated:
        login = request.user.id

        if request.method == 'POST':
            form = ReportFiltersForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date'] + datetime.timedelta(days=1)

                list_data = Add_data.objects.filter(author=login, date_time__range=(start_date, end_date))
                table = PersonTable(list_data)
                average_speed = get_average_speed(list_data)
            else:
                table, average_speed = user_data_table(login)
        else:
            table, average_speed = user_data_table(login)

        form = ReportFiltersForm(request.POST)

        title_tables = ["Author", "Distance, m", "Duration, min", "Speed", "Published date"]
        RequestConfig(request).configure(table)
        return render(request, 'myapp/data_list.html',
                      {"posts": table, "title_tables": title_tables, 'form': form, 'average_speed': average_speed})
    else:
        return HttpResponseRedirect('/login')


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


@login_required
def del_data(request, id_post):
    post = get_object_or_404(Add_data, pk=id_post)
    query = post.delete()
    return redirect("/data_list", request, query)


@login_required
def edit_data(request, id_post):
    post = get_object_or_404(Add_data, pk=id_post)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.author = request.user
            post.speed = get_speed(request.POST['distance'], request.POST['duration'])
            post.save()
            return redirect('data_list')
        else:
            print(form.is_valid())
    else:
        print(post)
        form = PostForm(instance=post)
    return render(request, 'myapp/add_data.html', {
        'form': form
    })


@login_required
def statistic(request):
    last_year = datetime.datetime.now().year - 1
    login = request.user.id

    data_set = Add_data.objects.filter(author=login, date_time__year__gte=last_year).annotate(
        week=ExtractWeek('date_time')
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

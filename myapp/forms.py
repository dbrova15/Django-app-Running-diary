from django import forms
from django.contrib.auth.models import User
from django.forms import SelectDateWidget
from django.utils import timezone

from .models import Add_data


class ReportFiltersForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget(), initial=timezone.now())


class PostForm(forms.ModelForm):
    date_time = forms.DateField(widget=SelectDateWidget(), initial=timezone.now())
    distance = forms.IntegerField(min_value=1)
    duration = forms.IntegerField(min_value=1)

    class Meta:
        model = Add_data
        fields = ('date_time', 'distance', 'duration')

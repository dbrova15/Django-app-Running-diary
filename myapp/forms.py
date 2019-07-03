from django import forms
from django.forms import SelectDateWidget
from django.utils import timezone

from .models import Post
from django.contrib.auth import authenticate


class ReportFiltersForm(forms.Form):
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget(), initial=timezone.now())


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('published_date', 'distance', 'duration')


# http://students.summerisgone.com/labs/lab4.html

class LoginForm(forms.Form):
    username = forms.CharField(label=u'Имя пользователя')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        if not self.errors:
            user = authenticate(username=cleaned_data['username'], password=cleaned_data['password'])
            if user is None:
                raise forms.ValidationError(u'Имя пользователя и пароль не подходят')
            self.user = user
        return cleaned_data

    def get_user(self):
        return self.user or None

from django import forms

from .models import Post
from django.contrib.auth import authenticate
from django.contrib.admin import widgets


class PostForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
        # self.fields['published_date'].widget = widgets.AdminSplitDateTime()


    class Meta:
        model = Post
        fields = ('published_date', 'distance', 'duration')
        # widgets = {
        #     'published_date': widgets.AdminSplitDateTime(),
        # }


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


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    email = forms.CharField(label='Почта пользователя', widget=forms.EmailInput)
    password1 = forms.CharField(label=u'Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'Повторите пароль', widget=forms.PasswordInput)

    def clean_username(self):
        self.username = self.cleaned_data.get('username')
        # TODO: проверить, что username не занят
        return self.cleaned_data

    def clean(self):
        self.password1 = self.cleaned_data.get('password1')
        self.password2 = self.cleaned_data.get('password2')
        # TODO: проверить, что пароли совпадают
        return self.cleaned_data

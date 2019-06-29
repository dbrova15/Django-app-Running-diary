from django.urls import path
from . import views

urlpatterns = [
    path('', views.readme, name='readme'),
    path('post_list', views.post_list, name='post_list'),
    path('signup', views.signup, name='signup'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('add_post', views.add_post, name='add_post'),
    path('del_post', views.del_post, name='del_post'),
    path('edit_post', views.edit_post, name='edit_post'),
]

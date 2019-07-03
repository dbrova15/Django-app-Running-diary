from django.urls import path, include

from Running_diary import settings
from . import views

urlpatterns = [
    path('', views.readme, name='readme'),
    path('data_list', views.data_list, name='data_list'),
    path('signup', views.SignUp.as_view(), name='signup'),
    path('add_data', views.add_data, name='add_data'),
    path('data_del/id=<int:id_post>', views.del_data, name='del_data'),
    path('edit_post/id=<int:id_post>', views.edit_data, name='edit_data'),
    path('statistic', views.statistic, name='statistic'),
    path('', include('social_django.urls', namespace='social')),
]

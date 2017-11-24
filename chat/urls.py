from django.conf.urls import url
from chat import views

urlpatterns = [
    url(r'^chief/$', views.chief, name='chief'),
    url(r'^chief/(?P<dialog_id>\S+)/$', views.show_dialog, name='dialog'),
    url(r'^chat/$', views.user_template, name='user_template'),
    url(r'^messages/get/$', views.get_messages, name='get_messages'),
    url(r'^messages/read/$', views.read_messages, name='read_messages'),
    url(r'^logout/', views.logout_a, name='logout'),
]

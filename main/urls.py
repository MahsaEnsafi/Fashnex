from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from main.views import *

app_name='main'

urlpatterns = [
    path('',index_view,name='index'),
    path('about/',about_view,name='about'),
    path('contact/',contact_view,name='contact')
]

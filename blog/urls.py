from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from blog.views import *

app_name='blog'

urlpatterns = [
    path('',bloghome_view,name='blog_home'),
    path('details/<id>',blogdetails_view,name='blog_details'),
    path("category/<str:cat_name>",bloghome_view,name='category'),
    path("tag/<str:tag_name>",bloghome_view,name='tag'),
    path("author/<str:username>",bloghome_view,name= "author"),
    path("search/",blogsearch_view,name='search'),
    path('newsletter/subscribe/', newsletter_subscribe, name='newsletter'),
    path('post/<int:id>/like/', post_like_toggle, name='post_like'),
]

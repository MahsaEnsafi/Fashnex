from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator
from taggit.managers import TaggableManager
from django.urls import reverse
from django.conf import settings

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
#-------------------------------------------------------------------------
class Post(models.Model):
    author=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    title=models.CharField(max_length=255)
    content=models.TextField()
    image=models.ImageField(upload_to='blog/',default='blog/default.jpg')
    created_date=models.DateTimeField(default=timezone.now())
    published_date=models.DateTimeField(null=True)
    updated_date=models.DateTimeField(auto_now=True)
    status=models.BooleanField(default=False)
    categories=models.ManyToManyField(Category)
    tags=TaggableManager()
    class Meta:
        ordering=['-created_date']
    def __str__(self):
        return self.title
    def excerpt(self, words=8, html=False):
        text = self.content or ""
        if html:
            return Truncator(text).words(int(words), html=True, truncate=" …")
        return Truncator(strip_tags(text)).words(int(words), truncate=" …")
    def get_absolute_url(self):
        return reverse('blog:blog_details',kwargs={'id':self.id})
#------------------------------------------------------------------------

#----------------------------------------------------------------------
class Comments(models.Model):
    post=models.ForeignKey(Post,related_name='comments',on_delete=models.CASCADE)
    name=models.CharField(max_length=255)
    subject=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField()
    message=models.TextField()
    created_date=models.DateTimeField(auto_now_add=True)
    updated_date=models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=False)
    class Meta:
        ordering=['created_date']
    def __str__(self):
        return self.name
    
#---------------------------------------------------------------------------
class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email
    
#----------------------------------------------------------------------------
class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('post', 'user') 
    def __str__(self):
        return f"{self.user} -> {self.post}"

from django.contrib import sitemaps
from blog.models import Post

class BlogSitmap(sitemaps.Sitemap):
    priority=0.5
    changefreq='weekly'
    def items(self):
        return Post.objects.filter(status=True)
    
    def lastmd(self,obj):
        return obj.published_date   
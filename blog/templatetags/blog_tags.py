from django import template
from taggit.models import Tag
from django.db.models import Count
from blog.models import Post,Category,Comments
register=template.Library()


@register.inclusion_tag('blog/blog_categories.html')
def postscategories():
    categories=Category.objects.all()
    posts=Post.objects.filter(status=1)
    cats_dict={}
    for name in categories:
        cats_dict[name]=posts.filter(categories=name).count()
    return {"categories":cats_dict}

@register.inclusion_tag('blog/blog_recentposts.html')
def recentposts(count=6):
    posts=Post.objects.filter(status=1).order_by("published_date")[:count]
    return {"posts":posts}

@register.inclusion_tag('blog/blog_tags.html')
def tag_list():
    tags = Tag.objects.annotate(
        num_posts=Count('taggit_taggeditem_items')
    ).order_by('-num_posts')        
    return {'tags': tags}
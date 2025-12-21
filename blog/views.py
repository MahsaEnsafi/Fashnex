from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.contrib.auth.decorators import login_required
from blog.models import Post,Comments,NewsletterSubscriber,Like
from blog.forms import ConmmentForm,NewsletterForm

# Create your views here.
def bloghome_view(request,cat_name:str=None,username:str=None,tag_name:str=None):
    posts = (Post.objects
             .filter(status=1,published_date__lte=timezone.now())
             .order_by('-published_date'))
    if cat_name:
        posts=posts.filter(categories__name=cat_name)
    if username:
        posts=posts.filter(author__username=username)
    if tag_name:
        posts=posts.filter(tags__name__in=[tag_name])
    posts=Paginator(posts,3)
    try:
        page_num=request.GET.get('page')
        posts=posts.page(page_num)
    except PageNotAnInteger:
        posts=posts.page(1)
    except EmptyPage:
        posts=posts.page(1)
    context={'posts':posts}
    return render(request,"blog/blog_home.html",context)
#---------------------------------------------------------------------
def blogdetails_view(request,id):
    
    if request.method == 'POST':
        form=ConmmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,'your comment submitted successfully')
        else:
            messages.add_message(request,messages.ERROR,'your comment did not submit.')
    
    post = get_object_or_404(
            Post,
            id=id,            
            status=1,
            published_date__lte=timezone.now()                     
        )
    comments=Comments.objects.filter(post=post.id,approved=True).order_by('-created_date')
    likes_qs = post.likes.select_related('user')  
    likes_count = likes_qs.count()
    first_liker = likes_qs.first().user if likes_count > 0 else None
    if request.user.is_authenticated:
        user_liked = Like.objects.filter(post=post, user=request.user).exists()
    else:
        user_liked = False
    
    prev_post=Post.objects.filter(
                created_date__lt=post.created_date,
                status=1,
                published_date__lte=timezone.now()).order_by('-created_date').first()
            
    next_post=Post.objects.filter(
                created_date__gt=post.created_date,
                status=1,
                published_date__lte=timezone.now()).order_by('created_date').first()
    form=ConmmentForm()
    context={
                'post':post,
                'comments':comments,
                'likes_count': likes_count,
                'first_liker': first_liker,
                'user_liked': user_liked,
                'form':form,
                'prev_post':prev_post,
                'next_post':next_post
                }
    return render(request,"blog/blog_details.html",context)
#--------------------------------------------------------------------------------

def blogsearch_view(request):
    posts=Post.objects.filter(status=1)
    if request.method =='GET':
        posts=posts.filter(content__contains=request.GET.get('s'))
    context={'posts':posts}
    return render(request,"blog/blog_home.html",context)

#---------------------------------------------------------------------------------
def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            obj, created = NewsletterSubscriber.objects.get_or_create(email=email)

            if created:
                messages.success(request, 'Successfully subscribed to our newsletter.')
            else:
                messages.info(request, 'This email is already subscribed.')

        else:
            messages.error(request, 'Invalid email address.')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)
#-------------------------------------------------------------------------------
@login_required
def post_like_toggle(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    like_qs = Like.objects.filter(post=post, user=user)
    if like_qs.exists():
        like_qs.delete()
    else:
        Like.objects.create(post=post, user=user)
    next_url = (
        request.POST.get('next')
        or request.META.get('HTTP_REFERER')
        or reverse('blog:blog_details', args=[id])
    )
    return redirect(next_url)
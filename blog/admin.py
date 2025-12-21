from django.contrib import admin
from blog.models import Post,Category,Comments,NewsletterSubscriber,Like
from django_summernote.admin import SummernoteModelAdmin

# Register your models here.
class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = 'created_date'
    empty_value_display = "-empty-"
    list_display = ["title", "status","published_date"]
    list_filter=("status",)
    ordering=["-created_date"]

admin.site.register(Post,PostAdmin)
admin.site.register(Category)
admin.site.register(Comments)
admin.site.register(NewsletterSubscriber)
admin.site.register(Like)

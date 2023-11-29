from django.contrib import admin
from .models import Post,Tag,Comments,Profile,WebsiteMeta
# Register your models here.
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(Profile)
admin.site.site_header = 'Blog Admin'
admin.site.site_title = 'Blog Admin'
admin.site.register(WebsiteMeta)

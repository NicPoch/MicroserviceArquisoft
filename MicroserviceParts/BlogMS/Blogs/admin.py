from django.contrib import admin
from .models import Blog,Comment,CommentOfComment,Post
# Register your models here.
admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(CommentOfComment)
admin.site.register(Post)
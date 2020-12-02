from djongo import models

# Create your models here.
class Blog(models.Model):
    _id=models.ObjectIdField()
    name=models.CharField(max_length=50,null=False,blank=False,default=None)
    user_id=models.TextField(null=False,default=None)
    intro=models.TextField()
    created=models.DateField(auto_created=True)
    objects=models.DjongoManager()
class Post(models.Model):
    _id=models.ObjectIdField()
    title=models.CharField(max_length=50,null=False,blank=False,default=None)
    blog_id=models.ForeignKey(to=Blog,on_delete=models.CASCADE)
    blog=models.ManyToOneRel(field=blog_id,to=Blog,related_name="posts",field_name="blog")
    created=models.DateField(auto_created=True)
    content=models.TextField(null=False,default=None,blank=False)
    objects=models.DjongoManager()
class Comment(models.Model):
    _id=models.ObjectIdField()
    user_id=models.TextField(null=False,default=None)
    post_id=models.ForeignKey(to=Post,on_delete=models.CASCADE)
    post=models.ManyToOneRel(field=post_id,to=Post,related_name="comments",field_name="post")
    comment=models.CharField(max_length=200,null=False,blank=False,default=None)
    likes=models.IntegerField(null=False,blank=False,default=0)
    dislikes=models.IntegerField(null=False,blank=False,default=0)
    created=models.DateField(auto_created=True)
    objects=models.DjongoManager()
class CommentOfComment(models.Model):
    _id=models.ObjectIdField()
    created=models.DateField(auto_created=True)
    user_id=models.TextField(null=False,default=None)
    comment_id=models.ForeignKey(to=Comment,on_delete=models.CASCADE)
    comment=models.ManyToOneRel(field=comment_id,to=Comment,related_name="comments",field_name="comment")
    commentOfComment=models.CharField(max_length=200,null=False,blank=False,default=None)
    likes=models.IntegerField(null=False,blank=False,default=0)
    dislikes=models.IntegerField(null=False,blank=False,default=0)
    objects=models.DjongoManager()
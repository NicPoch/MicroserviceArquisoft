from django.shortcuts import render
from .models import Blog,Comment,CommentOfComment,Post
from django.http import Http404,UnreadablePostError,JsonResponse,HttpResponse
import requests
import json
from BlogMS import settings
# Create your views here.
#-----------------------------------------------------------------------------------------------
#Check
#-----------------------------------------------------------------------------------------------
def check_user(data):
    try:
        r=requests.get(settings.PATH_VAR+"/"+data['id'],headers={"Accept":"application/json"})
        user=r.json()
        return True
    except Exception as identifier:
        return False
#-------------------------------------------------------------------------------------------------
#Get List
#-------------------------------------------------------------------------------------------------
def BlogsList(request):
    queryset = Blog.objects.all()
    context = list(queryset.values('_id', 'name', 'intro', 'created', 'user_id'))
    return JsonResponse(context, safe=False)  

def PostList(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    queryset = Post.objects.get(_id=data_json['_id'])
    context = list(queryset.values('_id', 'title', 'blog_id', 'created'))
    return JsonResponse(context, safe=False)

def CommentList(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    queryset = Comment.objects.aget(_id=data_json['_id'])
    context = list(queryset.values('_id', 'user_id', 'comment', 'created','likes','dislikes'))
    return JsonResponse(context, safe=False)    

def CommentOfCommentList(request):
    data = request.body.decode('utf-8')
    data_json = json.loads(data)
    queryset = CommentOfComment.objects.get(_id=data_json['_id'])
    context = list(queryset.values('_id', 'user_id', 'comment', 'created','likes','dislikes'))
    return JsonResponse(context, safe=False)   
#----------------------------------------------------------------------------------------------
#Get Post Detail
#----------------------------------------------------------------------------------------------
def PostDetail(request,id):
    pass
#----------------------------------------------------------------------------------------------
#Create
#----------------------------------------------------------------------------------------------
def CreateBlog(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        data_json = json.loads(data)
        if check_user(data_json) == True:
            try:
                blog = Blog()
                blog.intro = data_json['intro']
                blog.user_id = data_json['user_id']
                blog.name = data_json['name']
                blog.save()
                return JsonResponse(data=blog.__dict__,safe=False)    
            except Exception as identifier:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")

def CreatePost(request):
    if request.method =='POST':
        data=request.body.decode('utf-8')
        data_json=json.loads(data)
        if check_user(data_json) == True:
            try:
                if(Blog.objects.get(_id=data_json['blog_id']).check()):
                    post=Post()
                    post.blog_id=data_json['blog_id']
                    post.content=data_json['content']
                    post.title=data_json['title']
                    post.save()
                    return JsonResponse(data=post.__dict__,safe=False)    
                else:
                    return Http404("Error")    
            except Exception as identifier:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")

def CreateComment(request):
    if request.method =='POST':
        data=request.body.decode('utf-8')
        data_json=json.loads(data)
        if check_user(data_json) == True:
            try:
                if(Post.objects.get(_id=data_json['post_id']).check()):
                    comment=Comment()
                    comment.comment=data_json['comment']
                    comment.post_id=data_json['post_id']
                    comment.user_id=data_json['user_id']
                    comment.save()
                    return JsonResponse(data=comment.__dict__,safe=False)    
                else:
                    return Http404("Error")    
            except Exception as identifier:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")

def CreateCommentOfComment(request):
    if request.method =='POST':
        data=request.body.decode('utf-8')
        data_json=json.loads(data)
        if check_user(data_json) == True:
            try:
                if(Comment.objects.get(_id=data_json['comment_id']).check()):
                    comment=Comment()
                    comment.comment=data_json['comment']
                    comment.comment_id=data_json['comment_id']
                    comment.user_id=data_json['user_id']
                    comment.save()
                    return JsonResponse(data=comment.__dict__,safe=False)    
                else:
                    return Http404("Error")    
            except Exception as identifier:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")
#-------------------------------------------------------------------------------------------------
#Delete
#-------------------------------------------------------------------------------------------------
def DeleteBlog(request):
    if request.method=="DELETE":
        data=request.body.decode('utf-8')
        data_json=json.loads(data)
        if check_user(data_json)==True:
            if(Blog.objects.get(user_id=data_json['user_id'],_id=data_json['_id']).check()):
                Blog.objects.get(user_id=data_json['user_id'],name=data_json['_id']).delete()
                return HttpResponse(content="Success")
            else:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")

def DeletePost(request):
    if request.method=="DELETE":
        data=request.body.decode('utf-8')
        data_json=json.loads(data)
        if check_user(data_json)==True:
            if(Post.objects.get(user_id=data_json['user_id'],_id=data_json['_id']).check()):
                Blog.objects.get(user_id=data_json['user_id'],_id=data_json['_id']).delete()
                return HttpResponse(content="Success")
            else:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")

def DeleteComment(request):
    if request.method=="DELETE":
        data=request.body.decode('utf-8')
        data_json=json.loads(data)
        if check_user(data_json)==True:
            if(Comment.objects.get(user_id=data_json['user_id'],_id=data_json['_id']).check()):
                Comment.objects.get(user_id=data_json['user_id'],_id=data_json['_id']).delete()
                return HttpResponse(content="Success")
            else:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")
            
def DeleteCommentOfComment(request):
    if request.method=="DELETE":
        data=request.body.decode('utf-8')
        data_json=json.loads(data)
        if check_user(data_json)==True:
            if(CommentOfComment.objects.get(user_id=data_json['user_id'],_id=data_json['_id']).check()):
                CommentOfComment.objects.get(user_id=data_json['user_id'],_id=data_json['_id']).delete()
                return HttpResponse(content="Success")
            else:
                return Http404("Error")
        else:
            return Http404("User Doesn´t exist")
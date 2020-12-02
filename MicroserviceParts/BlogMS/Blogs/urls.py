from django.urls import path
from .views import BlogsList,CommentList,CommentOfCommentList,CreateBlog,CreateComment,CreateCommentOfComment,CreatePost,DeleteBlog,DeletePost,PostList,DeleteCommentOfComment,DeleteComment,PostDetail
urlpatterns = [
    path('blogs/',BlogsList,name="blogs"),
    path('blogs/<int:id_blog>/posts/',PostList,name="posts"),
    path('blogs/<int:id_blog>/posts/<int:id_post>/',PostDetail,name="post")
]
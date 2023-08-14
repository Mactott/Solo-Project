from django.urls import path
from . import views
urlpatterns = [
    path('', views.index),
    path('mypage/<page>', views.myPage),
    path('page/<page>', views.page),
    path('myposts', views.myPosts),
    path('theirposts/<int:id>', views.theirPosts),
    path('viewpost/<int:postId>', views.aPost),
    path('loggininfo', views.loggin_request),
    path('adduserinfo', views.add_user_request),
    path('newpostinfo', views.new_post_request),
    path('editinfo/<int:id>', views.edit_post_request),
    path('commentinfo', views.comment_request),
    path('delete/<int:id>', views.deleteById),
    path('loggin', views.loggin),
    path('adduser', views.create_user),
    path("loggout", views.loggout),
    path("newpost", views.newPost),
    path("comment/<int:id>", views.comment),
    path('editpost/<id>', views.editPost)
]
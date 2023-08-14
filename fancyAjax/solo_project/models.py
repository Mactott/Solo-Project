from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=500)

class Post(models.Model):
    user = models.ForeignKey(User, related_name="Post", on_delete= models.CASCADE)
    caption = models.CharField(max_length=50)
    text = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="Comment", on_delete= models.CASCADE)
    user = models.ForeignKey(User, related_name="Comments", on_delete= models.CASCADE)
    comment = models.CharField(max_length=75)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    edited = models.BooleanField(default=False)
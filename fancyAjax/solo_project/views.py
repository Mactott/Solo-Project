from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
import bcrypt
import re
import math
import requests
from django.http import JsonResponse
import json
from django.http import HttpResponseBadRequest
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from solo_project.models import User, Post, Comment
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from datetime import datetime



def index(request):
    all = {}
    count = Post.objects.count()
    countTen = math.ceil(count/10)
    split = list(range(0,countTen))
    posts = Post.objects.order_by("-created_at")[:10]
    all["posts"] = posts
    all["split"] = split
    all["last"] = countTen
    all["page"] = 0
    return render(request, "index.html", context=all)

def page(request, page):
    all = {}
    count = Post.objects.count()
    countTen = math.ceil(count/10)
    split = list(range(0,countTen))
    page_num = int(page)
    top = page_num*10
    bottom = (page_num+1)*10
    count = Post.objects.count()
    countTen = math.ceil(count/10)
    split = list(range(0,countTen))
    posts = Post.objects.order_by("-created_at")[top:bottom]
    all["posts"] = posts
    all["last"] = countTen
    all["split"] = split
    all["page"] = page_num
    return render(request, "index.html", context=all)

def aPost(request, postId):
    all = {}
    myPosts = Post.objects.get(id = postId)
    comments = Comment.objects.filter(post_id = myPosts.id)
    all["post"] = myPosts
    all["comments"] = comments
    return render(request, "post.html", context = all)

def myPosts(request):
    all = {}
    myPosts = Post.objects.filter(user = User.objects.get(id = request.session["id"])).order_by("-created_at")[:10]
    count = Post.objects.filter(user = User.objects.get(id = request.session["id"])).count()
    countTen = math.ceil(count/10)
    split = list(range(0,countTen))
    all["last"] = countTen
    all["posts"] = myPosts
    all["split"] = split
    all["page"] = 0
    all["posts"] = myPosts
    return render(request, "myPosts.html", context = all)

def myPage(request, page):
    all = {}
    count = Post.objects.filter(user = User.objects.get(id = request.session["id"])).count()
    countTen = math.ceil(count/10)
    split = list(range(0,countTen))
    page_num = int(page)
    top = page_num*10
    bottom = (page_num+1)*10
    count = Post.objects.count()
    countTen = math.ceil(count/10)
    split = list(range(0,countTen))
    myPosts = Post.objects.filter(user = User.objects.get(id = request.session["id"])).order_by("-created_at")[top:bottom]
    all["posts"] = myPosts
    all["last"] = countTen
    all["split"] = split
    all["page"] = page_num
    return render(request, "myPosts.html", context=all)

def theirPosts(request, id):
    all = {}
    user = User.objects.get(id = id)
    all["usered"] = user
    myPosts = Post.objects.filter(user_id = id).order_by("-created_at")
    all["posts"] = myPosts
    return render(request, "myPosts.html", context = all)

def loggout(request):
    request.session.clear()
    return redirect("/")

def loggin_request(request):
    all = {}
    all["modal"] = "loggin"
    all["form"] = "loggin"
    all["button"] = "Loggin"
    return render(request, "modal.html", context = all)

def add_user_request(request):
    all = {}
    all["modal"] = "addUser"
    all["form"] = "addUser"
    all["button"] = "Add User"
    return render(request, "modal.html", context = all)

def new_post_request(request):
    all = {}
    all["modal"] = "newPost"
    all["form"] = "newPost"
    all["button"] = "Add Post"
    all["blank"] = True
    return render(request, "modal.html", context = all)
    
def comment_request(request):
    all = {}
    all["modal"] = "comment"
    all["form"] = "comment"
    all["button"] = "Comment"
    return render(request, "modal.html", context = all)

def edit_post_request(request, id):
    post = Post.objects.get(id = int(id))
    all = {}
    all["modal"] = "newPost"
    all["form"] = "newPost"
    all["button"] = "Edit Post"
    all["post"] = post
    all["blank"] = False
    return render(request, "modal.html", context = all)

def loggin(request):
    email = request.POST["email"]
    password_raw = request.POST["password"]
    users = User.objects.all()
    for user in users:
        if user.email == email:
            if bcrypt.checkpw(password_raw.encode(), user.password.encode()) == True:
                request.session["id"] = user.id
                return HttpResponse("success")
            else:
                error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Loggin In</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Incorrect password</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
                return HttpResponse(error_content)
    error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Loggin In</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Email not found</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
    return HttpResponse(error_content)

def create_user(request):
    email = request.POST["email"]
    if not EMAIL_REGEX.match(email):
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Adding User</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Please enter a valid email</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    username = request.POST["username"]
    password_raw = request.POST["password"]
    password_raw2 = request.POST["confirm"]
    if len(password_raw) <7:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Adding User</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Password is too short</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    if password_raw != password_raw2:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Adding User</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Passwords dont match</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    users = User.objects.all()
    for user in users:
        if user.username == username:
            error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Adding User</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Username is already in use</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
            return HttpResponse(error_content)
        if user.email == email:
            error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Adding User</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Email is already in use</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
            return HttpResponse(error_content)
    password = bcrypt.hashpw(password_raw.encode(), bcrypt.gensalt()).decode()
    User.objects.create(email=email,password=password,username=username)
    request.session["id"] = User.objects.last().id
    return HttpResponse("success")


def newPost(request):
    caption = request.POST["caption"]
    text = request.POST["text"]
    if len(caption) > 50:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Posting</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Your caption was too long</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    if len(text) > 300:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Posting</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Your post was too long</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    if len(caption) < 10:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Posting</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Your caption was too short</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    post = Post.objects.create(text = text, caption = caption,user = User.objects.get(id = request.session["id"]))
    return HttpResponse("success" + " " + str(post.id))

def editPost(request, id):
    post = Post.objects.get(id=id)
    caption = request.POST["caption"]
    text = request.POST["text"]
    if len(caption) > 50:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Posting</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Your caption was too long</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    if len(text) > 300:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Posting</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Your post was too long</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    if len(caption) < 10:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Posting</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">Your caption was too short</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    post.caption = caption
    post.text = text
    post.edited = True
    post.save()
    return HttpResponse("success"+ " " + str(post.id))

def comment(request, id):
    post = Post.objects.get(id=id)
    comment = request.POST["comment"]
    if len(comment) < 1:
        error_content = '<div class="modal fade" id="errorModal" tabindex="-1" role="dialog"aria-labelledby="errorModalLabel" aria-hidden="true"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title" id="errorModalLabel">Issue Commenting</h5><button type="button" class="close" data-bs-dismiss="modal"aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">You need a comment to comment</div><div class="modal-footer"><button type="button" class="btn btn-secondary"data-bs-dismiss="modal">Close</button></div></div></div></div>'
        return HttpResponse(error_content)
    Comment.objects.create(comment = comment, user = User.objects.get(id = request.session["id"]), post = post)
    return HttpResponse("success"+ " " + str(post.id))

def deleteById(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return HttpResponse("success")
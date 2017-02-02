from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # same as doing Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST": #what exactly is the request and where is its method specified? Is this in the HTML method="POST"?
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})



@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST": # the URL doesn't change just because I posted a form. I need a redirect to do that. so we're still using the post_edit view after pressing submit
        form = PostForm(request.POST, instance=post) # if this is a POST request, then take the POST request data and enter it into a PostForm that refers to the post from the url
        if form.is_valid():
            post = form.save(commit=False) #saving the form turns it into a post object (with the same id etc as the one we're editing)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk) #then take me to the post_detail of this newly updated post
    else:
        form = PostForm(instance=post) #this variable needs to be named the same as the one below, but can differ from the one above. instance brings up existing data.
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail',pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list',pk=pk)

def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
#PostForm() is doing lots of clever things:
# 1. it can create a blank form
# 2. It can create a form that brings up details from a post if instance is specified
# 3. if request.POST is passed then it takes data from the form ready to be saved into a post.
# 4. if request.POST is passed and instance is passed, it takes the data to save into the specified post

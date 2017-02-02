from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import PostForm

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk) # same as doing Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST": #what exactly is the request and where is its method specified? Is this in the HTML method="POST"?
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST": # the URL doesn't change just because I posted a form. I need a redirect to do that. so we're still using the post_edit view after pressing submit
        form = PostForm(request.POST, instance=post) # if this is a POST request, then take the POST request data and enter it into a PostForm that refers to the post from the url
        if form.is_valid():
            post = form.save(commit=False) #saving the form turns it into a post object (with the same id etc as the one we're editing)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk) #then take me to the post_detail of this newly updated post
    else:
        form = PostForm(instance=post) #this variable needs to be named the same as the one below, but can differ from the one above. instance brings up existing data.
    return render(request, 'blog/post_edit.html', {'form': form})

#PostForm() is doing lots of clever things:
# 1. it can create a blank form
# 2. It can create a form that brings up details from a post if instance is specified
# 3. if request.POST is passed then it takes data from the form ready to be saved into a post.
# 4. if request.POST is passed and instance is passed, it takes the data to save into the specified post

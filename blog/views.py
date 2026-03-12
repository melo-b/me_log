from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from .models import Post, Comment
from .forms import CommentForm, PostForm

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PostSerializer

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here.

def blog_index(request):
    # Fetch all posts from the database, ordered by the newest first
    posts = Post.objects.all().order_by('-created_on')
    
    # Package the posts in a dictionary to send to the template
    context = {'posts': posts}
    
    # Render the HTML template and pass the context data to it
    return render(request, 'blog/index.html', context)

def post_detail(request, pk):
    # This securely fetches the post by its ID (primary key) or returns a 404 error if not found
    post = get_object_or_404(Post, pk=pk)
    
    # Fetch all comments linked to this specfic post
    comments = Comment.objects.filter(post=post).order_by('created_on')
    
    # Handle form submission
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Create a Comment object but don't save to the database yet
            comment.post = post # Link the comment to the current post
            comment.author = request.user.username # Set the author of the comment to the currently logged-in user's username
            comment.save() # Now save the comment to the database
            return redirect('post_detail', pk=post.pk) # Redirect to the same post detail page after saving the comment
        
    else:
            form = CommentForm() # If the form is not valid, create a new empty form
    
    context = {
        'post': post,
        'comments': comments,
        'form': form
        }
    return render(request, 'blog/post_detail.html', context)


@api_view(['GET'])
def api_post_list(request):
    """This endpoint returns a list of all blog posts in JSON format."""
    posts = Post.objects.all().order_by('-created_on')  # Fetch all posts, ordered by newest first
    serializer = PostSerializer(posts, many=True)  # Pass the database data to the translator. 'many=True' teslls it there are multiple posts to serialize
    return Response(serializer.data)  # Return the serialized data as a JSON response


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() # Save the new user to the database
            login(request, user) # Automatically log them in right after signing up!
            return redirect('blog_index') # Send them to the homepage
    else:
        form = UserCreationForm() # Show an empty registration form
    
    return render(request, 'registration/register.html', {'form': form})


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # SECURITY CHECK: Is the logged-in user the author?
    if request.user != post.author:
        raise PermissionDenied
        
    if request.method == 'POST':
        # request.FILES is required whenever your form handles image uploads
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # Pre-fill the form with the existing post data
        form = PostForm(instance=post)
        
    return render(request, 'blog/post_form.html', {'form': form, 'post': post})

def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    # SECURITY CHECK: Is the logged-in user the author?
    if request.user != post.author:
        raise PermissionDenied
        
    if request.method == 'POST':
        post.delete()
        return redirect('blog_index')
        
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
from django.shortcuts import render
from .models import Post

# Create your views here.

def blog_index(request):
    # Fetch all posts from the database, ordered by the newest first
    posts = Post.objects.all().order_by('-created_on')
    
    # Package the posts in a dictionary to send to the template
    context = {
        'posts': posts
    }
    
    # Render the HTML template and pass the context data to it
    return render(request, 'blog/index.html', context)


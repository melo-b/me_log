from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import CommentForm

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

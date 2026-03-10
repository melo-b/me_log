from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        # We specify exactly which fields we want to expose to the API
        fields = ['id', 'title', 'content', 'image', 'created_on']
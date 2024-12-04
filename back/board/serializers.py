from rest_framework import serializers
from .models import Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'content', 'author', 'author_nickname', 'created_at']
        read_only_fields = ['author', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()  # 댓글 필드 추가
    author_nickname = serializers.CharField(source='author.nickname', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'author_nickname', 'created_at', 'comments']
        read_only_fields = ['author', 'created_at']

    def get_comments(self, obj):
        comments = Comment.objects.filter(post=obj)
        return CommentSerializer(comments, many=True).data

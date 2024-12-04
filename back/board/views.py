from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print("요청 데이터:", self.request.data)  # 디버깅
        serializer.save(author=self.request.user)
        print("생성된 객체:", serializer.instance)  # 디버깅

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        print("요청 데이터:", self.request.data)  # 디버깅
        serializer.save(author=self.request.user)
        print("생성된 객체:", serializer.instance)  # 디버깅

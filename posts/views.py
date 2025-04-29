from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from posts.models import Post
from posts.serializers import PostsSerializer


class PostsViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

from rest_framework import serializers

from posts.models import Post


class PostsSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
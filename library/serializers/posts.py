from rest_framework import serializers

from library.models import Posts
from library.serializers.authors import AuthorShortInfoSerializer


class PostListSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Posts
        fields = [
            'id',
            'title',
            'moderated',
            'created_at',
            'author',
        ]

class PostRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class PostWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = [
            'id',
            'title',
            'body',
            'moderated',
            'author',
            'library',
            'created_at'
        ]




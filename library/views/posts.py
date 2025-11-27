from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from library.models import Posts
from library.serializers.posts import (
        PostListSerializer,
        PostRetrieveSerializer,
        PostWriterSerializer
    )

class PostViewSet(ModelViewSet):
    queryset = Posts.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer

        if self.action == 'retrive':
            return PostRetrieveSerializer

        #if self.action in ('update', 'create', 'partial_update'):
        else:
            return PostWriterSerializer

    def get_queryset(self):
        queryset = Posts.objects.all()
        x = self.request.query_params.get('moderated')
        if x is not None:
            queryset = queryset.filter(moderated=x)
        return queryset

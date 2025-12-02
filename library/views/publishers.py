# Варианты создания вьюшек
# 1. from rest_framework.decorators import api_view # def with @api_view()
# 2. from rest_framework.views import APIView
# 3. from rest_framework.generics import GenericAPIView
# 4. from rest_framework.viewsets import ModelViewSet


from django.db.models import Count
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status

from library.models import Publisher
from library.serializers import (
    PublisherCreateUpdateSerializer,
    PublisherDetailSerializer,
    PublisherListSerializer
)




class PublisherViewSet(ModelViewSet):
    queryset = Publisher.objects.all()

    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if 'list' in self.action:
            return PublisherListSerializer
        elif 'retrieve' in self.action:
            return PublisherDetailSerializer
        elif any(act in self.action for act in ('update', 'create', 'partial_update')):
            return PublisherCreateUpdateSerializer


    @action(methods=['get',], detail=False, url_path='statistic') # GET api/v1/publishers/statistic
    def get_statistic_per_publisher(self, request):
        pub_statistic = (
            Publisher.objects
            .values('name')
            .annotate(
                cnt_books=Count('books')
            )
        )

        return Response(
            data=pub_statistic,
            status=status.HTTP_200_OK
        )

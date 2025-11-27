from django.utils import timezone
from django.db.models import Count
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework import status


from library.models import Event
from library.serializers.events import (
    EventSerializer
    )

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        query_set = super().get_queryset()
        params = self.request.query_params
        library_id = params.get('library_id')
        if library_id:
            query_set = query_set.filter(library_id=library_id)

        x = params.get('type')
        today = timezone.localdate()
        if x and x == 'future':
            query_set = query_set.filter(date__gte=today)

        if x and x == 'past':
            query_set = query_set.filter(date__lt=today)
        return query_set

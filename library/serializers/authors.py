from rest_framework import serializers

from library.models import Author


class AuthorShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "rating"
        ]

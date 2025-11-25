from rest_framework import serializers

from library.models import User



class UserListSerializer(serializers.ModelSerializer):
    posts_cnt = serializers.IntegerField(
        required=False
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'role',
            'posts_cnt'
        ]

    def to_representation(self, instance: User):
        representation = super().to_representation(instance)

        if self.context['include_related']:
            representation['reviews'] = [
                {
                    "id": review.id,
                    "rating": review.rating,
                    "description": review.description,
                }
                for review in instance.reviews.all()
            ]

        return representation


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = [
            'password',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
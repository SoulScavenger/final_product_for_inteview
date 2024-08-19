from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from users.models import Subscription, CustomUser

from courses.models import Course

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор пользователей."""
    class Meta:
        model = User
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""


    class Meta:
        model = Subscription
        fields = (
            'user_id',
            'course_id',
            'course_title',
            'has_subscription'
            )
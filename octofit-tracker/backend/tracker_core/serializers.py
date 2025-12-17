from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Activity, Team

User = get_user_model()


class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ("id", "user", "display_name", "bio")


class ActivitySerializer(serializers.ModelSerializer):
    user = UserSummarySerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ("id", "user", "activity_type", "duration_minutes", "distance_km", "calories", "timestamp", "created")
        read_only_fields = ("id", "created", "user")


class TeamSerializer(serializers.ModelSerializer):
    members = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = ("id", "name", "members")

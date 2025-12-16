from django.db import models
from django.conf import settings


class Profile(models.Model):
    """User profile extending the built-in User model."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.display_name or self.user.username


class Team(models.Model):
    """A team that users can join for group challenges."""
    name = models.CharField(max_length=150)
    members = models.ManyToManyField(Profile, related_name="teams", blank=True)

    def __str__(self):
        return self.name


class Activity(models.Model):
    """A logged activity performed by a user."""
    ACTIVITY_CHOICES = [
        ("run", "Run"),
        ("walk", "Walk"),
        ("cycle", "Cycle"),
        ("swim", "Swim"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="activities")
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default="other")
    duration_minutes = models.PositiveIntegerField(help_text="Duration in minutes")
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    calories = models.PositiveIntegerField(null=True, blank=True)
    timestamp = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} - {self.activity_type} @ {self.timestamp.date()}"

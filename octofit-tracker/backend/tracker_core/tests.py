from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Profile, Activity
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from datetime import datetime

User = get_user_model()


class TrackerModelsAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", password="pass")
        self.profile = Profile.objects.create(user=self.user, display_name="Tester")
        self.client = APIClient()
        self.client.login(username="tester", password="pass")

    def test_create_activity_via_api(self):
        url = reverse('activity-list')
        data = {
            "activity_type": "run",
            "duration_minutes": 30,
            "distance_km": "5.00",
            "timestamp": datetime.now().isoformat(),
        }
        resp = self.client.post(url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        activity = Activity.objects.first()
        self.assertEqual(activity.user, self.user)

    def test_get_my_profile(self):
        url = reverse('profile-me')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['display_name'], 'Tester')

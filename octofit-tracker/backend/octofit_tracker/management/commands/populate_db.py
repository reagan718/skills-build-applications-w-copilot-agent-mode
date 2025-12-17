from django.core.management.base import BaseCommand
from tracker_core.models import Team, Activity, Profile
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete existing data

        get_user_model().objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        # LeaderboardEntry and Workout models do not exist yet, skip for now

        # Create Teams

        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create Users (superheroes)

        User = get_user_model()

        ironman = User.objects.create_user(username='ironman', email='ironman@marvel.com', password='password')
        captain = User.objects.create_user(username='captainamerica', email='cap@marvel.com', password='password')
        batman = User.objects.create_user(username='batman', email='batman@dc.com', password='password')
        superman = User.objects.create_user(username='superman', email='superman@dc.com', password='password')

        # Create Profile objects for each user
        Profile.objects.create(user=ironman, display_name='Iron Man', bio='Genius, billionaire, playboy, philanthropist.')
        Profile.objects.create(user=captain, display_name='Captain America', bio='The first Avenger.')
        Profile.objects.create(user=batman, display_name='Batman', bio='The Dark Knight.')
        Profile.objects.create(user=superman, display_name='Superman', bio='Man of Steel.')

        # Add users to teams via Profile
        marvel_profile_ironman = ironman.profile
        marvel_profile_captain = captain.profile
        dc_profile_batman = batman.profile
        dc_profile_superman = superman.profile
        marvel.members.add(marvel_profile_ironman, marvel_profile_captain)
        dc.members.add(dc_profile_batman, dc_profile_superman)

        # Create Activities

        from datetime import datetime
        Activity.objects.create(user=ironman, activity_type='run', duration_minutes=30, distance_km=5, timestamp=datetime.now())
        Activity.objects.create(user=captain, activity_type='cycle', duration_minutes=60, distance_km=20, timestamp=datetime.now())
        Activity.objects.create(user=batman, activity_type='swim', duration_minutes=45, distance_km=2, timestamp=datetime.now())
        Activity.objects.create(user=superman, activity_type='run', duration_minutes=50, distance_km=10, timestamp=datetime.now())

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))

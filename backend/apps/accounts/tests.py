from rest_framework.test import APITestCase
from apps.accounts.models import User
from apps.game.models import PlayerProgress


class ProfileUpdateTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user('player@example.com', 'safe-password', nickname='player')
        self.progress = PlayerProgress.objects.create(user=self.user, score=123)
        self.client.force_authenticate(self.user)

    def test_changing_nickname_preserves_player_progress(self):
        response = self.client.patch('/api/v1/users/me/profile', {'nickname': 'new_player'}, format='multipart')

        self.assertEqual(response.status_code, 200)
        self.progress.refresh_from_db()
        self.user.refresh_from_db()
        self.assertEqual(self.user.nickname, 'new_player')
        self.assertEqual(self.progress.score, 123)
        self.assertEqual(self.progress.user_id, self.user.id)


class PublicLeaderboardTests(APITestCase):
    def test_leaderboard_is_available_without_authentication(self):
        user = User.objects.create_user('rank@example.com', 'safe-password', nickname='rank_player')
        PlayerProgress.objects.create(user=user, score=50)

        response = self.client.get('/api/v1/game/leaderboard')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0], {'position': 1, 'nickname': 'rank_player', 'score': 50})

from rest_framework.test import APITestCase

from apps.accounts.models import User
from apps.game.models import PlayerProgress, PlayerUpgrade


class UpgradeApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            'upgrades@example.com',
            'safe-password',
            nickname='upgrade_player',
        )
        self.progress = PlayerProgress.objects.create(user=self.user, score=300)
        self.client.force_authenticate(self.user)

    def test_lists_catalog_and_current_total_cps(self):
        response = self.client.get('/api/v1/game/upgrades')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['upgrades']), 3)
        self.assertEqual(response.data['upgrades'][0]['key'], 'clicker')
        self.assertEqual(response.data['upgrades'][0]['quantity'], 0)
        self.assertEqual(response.data['total_clicks_per_second'], 0)

    def test_purchase_deducts_score_and_increases_quantity(self):
        response = self.client.post('/api/v1/game/upgrades/clicker/purchase')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['score'], 285)
        self.assertEqual(response.data['upgrades'][0]['quantity'], 1)
        self.assertEqual(response.data['total_clicks_per_second'], 0.1)
        self.assertEqual(
            PlayerUpgrade.objects.get(user=self.user, upgrade_type='clicker').quantity,
            1,
        )

    def test_purchase_rejects_insufficient_score(self):
        self.progress.score = 10
        self.progress.save(update_fields=['score'])

        response = self.client.post('/api/v1/game/upgrades/clicker/purchase')

        self.assertEqual(response.status_code, 400)
        self.progress.refresh_from_db()
        self.assertEqual(self.progress.score, 10)
        self.assertFalse(PlayerUpgrade.objects.filter(user=self.user).exists())

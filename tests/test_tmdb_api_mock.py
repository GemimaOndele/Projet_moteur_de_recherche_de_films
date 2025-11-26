import unittest
from unittest.mock import patch
import code.tmdb_api as tmdb

class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code
    def json(self):
        return self._json_data

class TestTMDBAPIMock(unittest.TestCase):
    def setUp(self):
        # Create a minimal TMDB JSON response
        self.sample_data = {
            "poster_path": "/poster.jpg",
            "backdrop_path": "/backdrop.jpg",
            "overview": "Un film d'exemple en français.",
            "videos": {"results": [{"type": "Trailer", "site": "YouTube", "key": "ABC123"}]},
            "runtime": 100,
            "budget": 100000,
            "revenue": 500000,
            "watch/providers": {"results": {"FR": {"flatrate": [{"provider_name": "Netflix", "logo_path": "/netflix.jpg"}]}}}
        }

    def fake_requests_get(self, url, params=None, headers=None, timeout=5):
        # Return our sample data for any TMDB call
        return FakeResponse(self.sample_data, status_code=200)

    @patch('code.tmdb_api.requests.get')
    def test_enrichir_film_avec_api_mock(self, mock_get):
        mock_get.side_effect = self.fake_requests_get
        film = {"id": 123}
        res = tmdb.enrichir_film_avec_api(film)

        self.assertEqual(res.get('poster_url'), tmdb.TMDB_POSTER_BASE + "/poster.jpg")
        self.assertEqual(res.get('backdrop_url'), tmdb.TMDB_POSTER_BASE + "/backdrop.jpg")
        self.assertEqual(res.get('trailer_key'), 'ABC123')
        self.assertIn('youtube', res.get('trailer_url'))
        self.assertEqual(res.get('overview_fr'), 'Un film d\'exemple en français.')
        self.assertEqual(res.get('runtime'), 100)
        self.assertEqual(res.get('budget'), 100000)
        self.assertEqual(res.get('revenue'), 500000)
        self.assertIsInstance(res.get('streaming_links'), list)
        self.assertGreater(len(res.get('streaming_links')), 0)

if __name__ == '__main__':
    unittest.main()

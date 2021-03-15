import sys  # noqa: E402
sys.path.append('../')
import data_processing.download_nutritionix_data as dnd  # noqa: E402
import unittest  # noqa: E402
from unittest import mock  # noqa: E402


class TestDataDownload(unittest.TestCase):
    def test_download_valid(self):
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value.ok = True
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "key1": "value1",
                "hits": ['test', 'test2']
                }
            result = dnd.fetch_data_from_nutritionix()
            mock_post.assert_called_once_with
            assert(len(result) == 2)

    def test_download_invalid(self):
        with mock.patch('requests.post') as mock_post:
            mock_post.return_value.ok = False
            mock_post.return_value.status_code = 404
            mock_post.return_value.json.return_value = {
                "key1": "value1",
                "hits": ['test', 'test2']
                }
            result = dnd.fetch_data_from_nutritionix()
            mock_post.assert_called_once()
            assert(len(result) != 2)


if __name__ == '__main__':
    unittest.main()

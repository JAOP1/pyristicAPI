import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from .main import app


@patch('app.settings.LOCAL_FILE_STORAGE', '__test__/')
class TestCreateFileRoute(unittest.TestCase):
    """
    Test suite for create file route.
    """
    CLIENT = TestClient(app)

    def test_create_available_files(self):
        response = self.CLIENT.post('/create-file/function', data={'content':'Test file'})
        print(response)

if __name__ == '__main__':
    unittest.main(verbosity=3)
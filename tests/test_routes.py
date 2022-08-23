import unittest
from unittest.mock import patch
import os
from fastapi import HTTPException
from fastapi.testclient import TestClient
import json
import main


class TestCreateFileRoute(unittest.TestCase):
    """
    Test suite for create file route.
    """
    CLIENT = TestClient(main.app)

    @patch('settings.LOCAL_FILE_STORAGE','tests/')
    def test_create_available_files(self):
        """
        Tests for the /create-file/ route.
        """
        #It should return a valid file when the user make a post request.
        for file_name in ['function','constraints', 'search_space']:
            response = self.CLIENT.post(f'/create-file/{file_name}', json={'content':'Test file'})
            self.assertEqual(response.status_code,200)
            self.assertEqual(os.path.exists(f"tests/{file_name}.py"), True)
            os.remove(f"tests/{file_name}.py")

    def test_create_file_fail(self):
        """
        Tests when the request couldn't complete because not is an accepted file name.
        """

        #It should return exception when the request path isn't valid.
        response = self.CLIENT.post(f'/create-file/evolutionary', json={'content':'Test file'})
        self.assertEqual(response.status_code,422)
        dict_response = json.loads(response.content.decode('utf-8'))
        self.assertTrue(
            "value is not a valid enumeration member" in dict_response['detail'][0]['msg'])

if __name__ == '__main__':
    unittest.main(verbosity=3)
import unittest
from unittest.mock import patch
from fastapi import HTTPException
from fastapi.testclient import TestClient
import json
import main


class TestCreateFileRoute(unittest.TestCase):
    """
    Test suite for create file route.
    """

    CLIENT = TestClient(main.app)

    @patch("main.utils.create_file")
    def test_create_available_files(self, mock_create_file):
        """
        Tests for the /create-file/ route.
        """
        # It should return a valid file when the user make a post request.
        for file_name in ["function", "constraints", "search_space"]:
            response = self.CLIENT.post(
                f"/create-file/{file_name}", json={"content": "Test file"}
            )
            self.assertEqual(response.status_code, 200)
        # It should raise an exception when the creation of file fail.
        mock_create_file.side_effect = Exception("Something has failed.")
        response = self.CLIENT.post(
            f"/create-file/{file_name}", json={"content": "Test file"}
        )
        self.assertEqual(response.status_code, 500)
        dict_response = json.loads(response.content.decode("utf-8"))
        self.assertTrue("Something has failed." == dict_response["detail"])

    def test_create_file_fail(self):
        """
        Tests when the request couldn't complete because not is an accepted file name.
        """

        # It should return exception when the request path isn't valid.
        response = self.CLIENT.post(
            f"/create-file/evolutionary", json={"content": "Test file"}
        )
        self.assertEqual(response.status_code, 422)
        dict_response = json.loads(response.content.decode("utf-8"))
        self.assertTrue(
            "value is not a valid enumeration member"
            in dict_response["detail"][0]["msg"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=3)

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi.exceptions import HTTPException, RequestValidationError
import routes.utilities_routes as util_router


class TestUtilitiesRoute(unittest.TestCase):
    """
    Test suite for create file route.
    """

    CLIENT = TestClient(util_router.utilities_router)

    @patch("routes.utilities_routes.create_file")
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
            self.assertEqual(response.json(), f"Created with success {file_name}")
        # It should raise an exception when the creation of file fail.
        mock_create_file.side_effect = Exception("Something has failed.")
        with self.assertRaises(HTTPException):
            self.CLIENT.post(f"/create-file/{file_name}", json={"content": "Test file"})
        # It should return exception when the request path isn't valid.
        with self.assertRaises(RequestValidationError):
            self.CLIENT.post("/create-file/evolutionary", json={"content": "Test file"})


if __name__ == "__main__":
    unittest.main(verbosity=3)

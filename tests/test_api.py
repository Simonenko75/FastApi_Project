import unittest
from fastapi.testclient import TestClient

from fastapi_app.main import app as web_app


class APITestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.client = TestClient(web_app)

    def tearDown(self) -> None:
        pass

    def test_main_url(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_create_user(self) -> None:
        user_data = {
            "user": {
                "email": "testiggg@tgggs.com",
                "password": "gggg",
                "first_name": "Jofghdn3",
                "last_name": "Dodgfhe2",
                "nickname": "joydgfh321"
            }
        }

        response = self.client.post("/users", json=user_data)
        self.assertEqual(response.status_code, 200)

    def test_create_post(self) -> None:
        post_data = {
            "post": {
                "title": "java",
                "subtitle": "jdk",
                "author": "java rush",
                "content": "java is language...",
                "completed": False
            }
        }

        response = self.client.post("/posts", json=post_data)
        self.assertEqual(response.status_code, 200)


# if __name__ == '__main__':
#     unittest.main()
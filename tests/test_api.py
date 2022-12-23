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

    """Для проверки получения пользователя надо использовать существующий token"""
    def test_get_token_url(self):
        token_data = "b67872f9-03fe-4145-a734-f76f89d1bb84"
        response = self.client.get(f"/get/user/by/token?token={token_data}")
        self.assertEqual(response.status_code, 200)

    """Для проверки получения пользователя надо использовать существующий id"""
    def test_get_user_by_id_url(self):
        response = self.client.get("/get/user/by/id/3")
        self.assertEqual(response.status_code, 200)

    """Для проверки получения поста надо использовать существующий id"""
    def test_get_post_by_id_url(self):
        response = self.client.get("/get/post/by/id/12")
        self.assertEqual(response.status_code, 200)

    """Для проверки получения коментария надо использовать существующий id"""
    def test_get_comment_by_id_url(self):
        response = self.client.get("/get/comment/by/id/2")
        self.assertEqual(response.status_code, 200)

    """Все тести что закоментировани ниже полностю рабочие, если разкоментировать их то они отработают.
        Но для избежания ошибок данные желательно вводить вручную, смотря на коменти возле метода """

    """Для проверки добавления пользователя надо использовать уникальный почтовий адрес"""
    # def test_create_user(self) -> None:
    #     user_data = {
    #         "email": "testiggg12345@tgggs.com",
    #         "password": "gggg12345",
    #         "first_name": "Jofghdn345",
    #         "last_name": "Dodgfhe245",
    #         "nickname": "joydgfh3214"
    #     }
    #
    #     response = self.client.post("/create/user", json=user_data)
    #     self.assertEqual(response.status_code, 200)

    """Для проверки добавления поста надо использовать существующий почтовий адрес"""
    # def test_create_post(self) -> None:
    #     post_data = {
    #         "title": "java12345",
    #         "subtitle": "jdk12345",
    #         "author_email": "777@gmail.com",
    #         "content": "java is language 12345...",
    #         "completed": True
    #     }
    #
    #     response = self.client.post("/create/post", json=post_data)
    #     self.assertEqual(response.status_code, 200)

    """Для проверки добавления коментария надо использовать
        существующий почтовий адрес и существующий title and subtitle"""
    # def test_create_comment(self) -> None:
    #     post_data = {
    #         "title": "java1234",
    #         "subtitle": "jdk1234",
    #         "author_email": "777@gmail.com",
    #         "comment_text": "java is language 12344444444444555555..."
    #     }
    #
    #     response = self.client.post("/create/comment", json=post_data)
    #     self.assertEqual(response.status_code, 200)

    """Для проверки изменения данных о пользователе надо использовать существующий id пользователя"""
    # def test_update_user(self) -> None:
    #     user_data = {
    #         "email": "string1234@tgggs.com",
    #         "password": "ggg21234g12345",
    #         "first_name": "Jo1e234fghdn345",
    #         "last_name": "Do1e234dgfhe245",
    #         "nickname": "joy1e23dgfh3214"
    #     }
    #
    #     response = self.client.put("/update/user/11", json=user_data)
    #     self.assertEqual(response.status_code, 200)

    """Для проверки изменения данных о посте надо использовать существующий id поста и author_email"""
    # def test_update_post(self) -> None:
    #     post_data = {
    #         "title": "java23412345",
    #         "subtitle": "jdk23412345",
    #         "author_email": "qwerty",
    #         "content": "Java 123is123 language 2243412345...",
    #         "completed": True
    #     }
    #
    #     response = self.client.put("/update/post/7", json=post_data)
    #     self.assertEqual(response.status_code, 200)

    """Для проверки изменения данных о коментарие надо использовать
        существующий id, почтовий адрес и существующий title and subtitle"""
    # def test_update_comment(self) -> None:
    #     post_data = {
    #         "title": "java1234",
    #         "subtitle": "jdk1234",
    #         "author_email": "777@gmail.com",
    #         "comment_text": "java 123is123 7language7 ..."
    #     }
    #
    #     response = self.client.put("/update/comment/3", json=post_data)
    #     self.assertEqual(response.status_code, 200)

    """Для проверки получения пользователя надо использовать существующий id"""
    # def test_delete_user_by_id_url(self):
    #     response = self.client.delete("/delete/user/6")
    #     self.assertEqual(response.status_code, 200)

    """Для проверки получения поста надо использовать существующий id"""
    # def test_delete_post_by_id_url(self):
    #     response = self.client.delete("/delete/post/8")
    #     self.assertEqual(response.status_code, 200)

    """Для проверки получения коментария надо использовать существующий id"""
    # def test_delete_comment_by_id_url(self):
    #     response = self.client.delete("/delete/comment/5")
    #     self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
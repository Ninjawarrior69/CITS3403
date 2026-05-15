import unittest

from app import create_app, db
from app.config import TestingConfig
from app.models import User


class BackendUnitTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config.from_object(TestingConfig)

        self.app_ctx = self.app.app_context()
        self.app_ctx.push()

        db.create_all()

    def test_app_is_created(self):
        self.assertIsNotNone(self.app)
        
    def test_password_is_hashed(self):
        user = User(
            username="testuser",
            email="test@example.com"
        )
        user.set_password("password123")

        self.assertNotEqual(user.password_hash, "password123")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.check_password("wrongpassword"))


if __name__ == "__main__":
    unittest.main()
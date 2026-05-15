import unittest

from app import create_app, db
from app.config import TestingConfig
from app.models import User


class BackendUnitTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)

        self.app_ctx = self.app.app_context()
        self.app_ctx.push()

        db.create_all()

    def test_app_is_created(self):
        self.assertIsNotNone(self.app)
        
    def test_password_is_hashed(self):
        user = User(
            name="Test User",
            username="testuser",
            email="test@example.com"
        )
        user.set_password("password123")

        self.assertNotEqual(user.password_hash, "password123")
        self.assertTrue(user.check_password("password123"))
        self.assertFalse(user.check_password("wrongpassword"))

    def test_user_can_be_created(self):
        user = User(
            name="Test User",
            username="testuser",
            email="test@example.com"
        )
        user.set_password("password123")

        db.session.add(user)
        db.session.commit()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, "test@example.com")
        self.assertTrue(saved_user.check_password("password123"))

    def add_user(self, name="Test User", username="testuser", email="test@example.com", password="password123"):
        user = User(
            name=name,
            username=username,
            email=email
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user
    
    def test_login_with_correct_password(self):
        user = self.add_user()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user)
        self.assertTrue(saved_user.check_password("password123"))


    def test_login_with_wrong_password(self):
        user = self.add_user()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user)
        self.assertFalse(saved_user.check_password("wrongpassword"))

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()


if __name__ == "__main__":
    unittest.main()
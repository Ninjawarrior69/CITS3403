import unittest

from app import create_app, db
from app.config import TestingConfig
from app.models import User, Book, Comment, Rating, ShelfItem


class BackendUnitTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)

        self.app_ctx = self.app.app_context()
        self.app_ctx.push()

        db.create_all()

    def add_user(
        self,
        name="Test User",
        username="testuser",
        email="test@example.com",
        password="password123"
    ):
        user = User(
            name=name,
            username=username,
            email=email
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user
    
    def add_book(self, title="Test Book", author="Test Author"):
        book = Book(
            title=title,
            author=author,
            description="Test description",
            rating=0,
            reads=0
        )

        db.session.add(book)
        db.session.commit()

        return book

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
        user = self.add_user()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user)
        self.assertEqual(saved_user.email, "test@example.com")
        self.assertTrue(saved_user.check_password("password123"))

    def test_login_with_correct_password(self):
        self.add_user()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user)
        self.assertTrue(saved_user.check_password("password123"))

    def test_login_with_wrong_password(self):
        self.add_user()

        saved_user = User.query.filter_by(username="testuser").first()

        self.assertIsNotNone(saved_user)
        self.assertFalse(saved_user.check_password("wrongpassword"))

    def test_book_can_be_created(self):
        book = self.add_book()

        saved_book = Book.query.filter_by(title="Test Book").first()

        self.assertIsNotNone(saved_book)
        self.assertEqual(saved_book.author, "Test Author")


    def test_review_creation_works(self):
        user = self.add_user()
        book = self.add_book()

        review = Comment(
            user_id=user.id,
            book_id=book.id,
            username=user.username,
            stars=5,
            text="Great book."
        )

        db.session.add(review)
        db.session.commit()

        saved_review = Comment.query.filter_by(user_id=user.id, book_id=book.id).first()

        self.assertIsNotNone(saved_review)
        self.assertEqual(saved_review.text, "Great book.")
        self.assertEqual(saved_review.stars, 5)


    def test_review_editing_works(self):
        user = self.add_user()
        book = self.add_book()

        review = Comment(
            user_id=user.id,
            book_id=book.id,
            username=user.username,
            stars=4,
            text="Original review."
        )

        db.session.add(review)
        db.session.commit()

        review.text = "Updated review."
        review.stars = 5
        db.session.commit()

        saved_review = Comment.query.filter_by(user_id=user.id, book_id=book.id).first()

        self.assertEqual(saved_review.text, "Updated review.")
        self.assertEqual(saved_review.stars, 5)


    def test_rating_creation_works(self):
        user = self.add_user()
        book = self.add_book()

        rating = Rating(
            user_id=user.id,
            book_id=book.id,
            username=user.username,
            stars=4
        )

        db.session.add(rating)
        db.session.commit()

        saved_rating = Rating.query.filter_by(user_id=user.id, book_id=book.id).first()

        self.assertIsNotNone(saved_rating)
        self.assertEqual(saved_rating.stars, 4)


    def test_rating_update_does_not_create_duplicate(self):
        user = self.add_user()
        book = self.add_book()

        rating = Rating(
            user_id=user.id,
            book_id=book.id,
            username=user.username,
            stars=3
        )

        db.session.add(rating)
        db.session.commit()

        existing_rating = Rating.query.filter_by(user_id=user.id, book_id=book.id).first()
        existing_rating.stars = 5
        db.session.commit()

        ratings = Rating.query.filter_by(user_id=user.id, book_id=book.id).all()

        self.assertEqual(len(ratings), 1)
        self.assertEqual(ratings[0].stars, 5)


    def test_shelf_item_creation_works(self):
        user = self.add_user()
        book = self.add_book()

        shelf_item = ShelfItem(
            user_id=user.id,
            book_id=book.id,
            status="To Be Read"
        )

        db.session.add(shelf_item)
        db.session.commit()

        saved_item = ShelfItem.query.filter_by(user_id=user.id, book_id=book.id).first()

        self.assertIsNotNone(saved_item)
        self.assertEqual(saved_item.status, "To Be Read")


    def test_shelf_status_update_works(self):
        user = self.add_user()
        book = self.add_book()

        shelf_item = ShelfItem(
            user_id=user.id,
            book_id=book.id,
            status="To Be Read"
        )

        db.session.add(shelf_item)
        db.session.commit()

        shelf_item.status = "Read"
        db.session.commit()

        saved_item = ShelfItem.query.filter_by(user_id=user.id, book_id=book.id).first()

        self.assertEqual(saved_item.status, "Read")

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()


if __name__ == "__main__":
    unittest.main()
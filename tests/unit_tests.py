import unittest

from app import create_app, db
from app.config import TestingConfig
from app.models import User, Book, Comment, Rating, ShelfItem
from app.helpers.validation_helpers import (
    is_valid_rating,
    is_valid_review_text,
    is_valid_shelf_status,
)
from app.helpers.review_helpers import create_or_update_review


class BackendUnitTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestingConfig)

        self.app_ctx = self.app.app_context()
        self.app_ctx.push()

        self.client = self.app.test_client()

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
    
    def login_as(self, user):
        with self.client.session_transaction() as sess:
            sess["_user_id"] = str(user.id)
            sess["_fresh"] = True

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
    
    def test_rating_validation_accepts_valid_values(self):
        self.assertTrue(is_valid_rating(1))
        self.assertTrue(is_valid_rating(5))
        self.assertTrue(is_valid_rating(0, allow_zero=True))


    def test_rating_validation_rejects_invalid_values(self):
        self.assertFalse(is_valid_rating(None))
        self.assertFalse(is_valid_rating(0))
        self.assertFalse(is_valid_rating(6))
        self.assertFalse(is_valid_rating(-1))


    def test_review_text_validation(self):
        self.assertTrue(is_valid_review_text("Good book."))
        self.assertFalse(is_valid_review_text(""))
        self.assertFalse(is_valid_review_text("   "))
        self.assertFalse(is_valid_review_text(None))


    def test_shelf_status_validation(self):
        self.assertTrue(is_valid_shelf_status("Read"))
        self.assertTrue(is_valid_shelf_status("Currently Reading"))
        self.assertTrue(is_valid_shelf_status("To Be Read"))
        self.assertTrue(is_valid_shelf_status("Did Not Finish"))
        self.assertTrue(is_valid_shelf_status("remove"))
        self.assertFalse(is_valid_shelf_status("Invalid Status"))

    def test_create_or_update_review_creates_review(self):
        user = self.add_user()
        book = self.add_book()

        create_or_update_review(
            book_id=book.id,
            stars=5,
            text="Great book.",
            user=user
        )

        db.session.commit()

        saved_review = Comment.query.filter_by(
            user_id=user.id,
            book_id=book.id
        ).first()

        self.assertIsNotNone(saved_review)
        self.assertEqual(saved_review.text, "Great book.")
        self.assertEqual(saved_review.stars, 5)

    def test_create_or_update_review_updates_existing_review(self):
        user = self.add_user()
        book = self.add_book()

        create_or_update_review(
            book_id=book.id,
            stars=4,
            text="Original review.",
            user=user
        )
        db.session.commit()

        create_or_update_review(
            book_id=book.id,
            stars=5,
            text="Updated review.",
            user=user
        )
        db.session.commit()

        reviews = Comment.query.filter_by(
            user_id=user.id,
            book_id=book.id
        ).all()

        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0].text, "Updated review.")
        self.assertEqual(reviews[0].stars, 5)

    def test_user_cannot_update_another_users_review(self):
        user_a = self.add_user(
            name="User A",
            username="usera",
            email="usera@example.com"
        )
        user_b = self.add_user(
            name="User B",
            username="userb",
            email="userb@example.com"
        )
        book = self.add_book()

        # User B already has a review
        review = Comment(
            user_id=user_b.id,
            book_id=book.id,
            username=user_b.username,
            stars=4,
            text="User B original review."
        )
        db.session.add(review)
        db.session.commit()

        # User A tries to update User B's review
        create_or_update_review(
            book_id=book.id,
            stars=1,
            text="User A should not be able to change this.",
            user=user_a
        )
        db.session.commit()

        user_b_review = Comment.query.filter_by(
            user_id=user_b.id,
            book_id=book.id
        ).first()

        self.assertEqual(user_b_review.text, "User B original review.")
        self.assertEqual(user_b_review.stars, 4)

    def test_user_cannot_update_another_users_progress(self):
        user_a = self.add_user(
            name="User A",
            username="usera",
            email="usera@example.com"
        )
        user_b = self.add_user(
            name="User B",
            username="userb",
            email="userb@example.com"
        )
        book = self.add_book()

        shelf_item = ShelfItem(
            user_id=user_b.id,
            book_id=book.id,
            status="Currently Reading",
            current_page=10
        )

        db.session.add(shelf_item)
        db.session.commit()

        self.login_as(user_a)

        response = self.client.post(
            f"/shelf/{shelf_item.id}/progress",
            data={"current_page": 50},
            follow_redirects=False
        )

        db.session.expire_all()
        saved_item = ShelfItem.query.get(shelf_item.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(saved_item.current_page, 10)
        self.assertEqual(saved_item.status, "Currently Reading")

    def test_user_cannot_delete_another_users_review(self):
        user_a = self.add_user(
            name="User A",
            username="usera",
            email="usera@example.com"
        )
        user_b = self.add_user(
            name="User B",
            username="userb",
            email="userb@example.com"
        )
        book = self.add_book()

        review = Comment(
            user_id=user_b.id,
            book_id=book.id,
            username=user_b.username,
            stars=4,
            text="User B review."
        )

        db.session.add(review)
        db.session.commit()

        self.login_as(user_a)

        response = self.client.post(
            f"/review/{review.id}/delete",
            follow_redirects=False
        )

        db.session.expire_all()
        saved_review = Comment.query.get(review.id)

        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(saved_review)
        self.assertEqual(saved_review.text, "User B review.")

    def test_book_view_count_increases_first_time(self):
        book = self.add_book()

        response = self.client.get(f"/book/{book.id}")

        self.assertEqual(response.status_code, 200)

        db.session.expire_all()
        saved_book = Book.query.get(book.id)

        self.assertEqual(saved_book.reads, 1)


    def test_same_book_only_counts_once_per_session(self):
        book = self.add_book()

        self.client.get(f"/book/{book.id}")
        self.client.get(f"/book/{book.id}")
        self.client.get(f"/book/{book.id}")

        db.session.expire_all()
        saved_book = Book.query.get(book.id)

        self.assertEqual(saved_book.reads, 1)


    def test_different_books_each_increase_once(self):
        book1 = self.add_book(title="Test Book One", author="Author One")
        book2 = self.add_book(title="Test Book Two", author="Author Two")

        self.client.get(f"/book/{book1.id}")
        self.client.get(f"/book/{book2.id}")

        db.session.expire_all()
        saved_book1 = Book.query.get(book1.id)
        saved_book2 = Book.query.get(book2.id)

        self.assertEqual(saved_book1.reads, 1)
        self.assertEqual(saved_book2.reads, 1)


    def test_new_session_can_count_same_book_again(self):
        book = self.add_book()

        self.client.get(f"/book/{book.id}")

        new_client = self.app.test_client()
        new_client.get(f"/book/{book.id}")

        db.session.expire_all()
        saved_book = Book.query.get(book.id)

        self.assertEqual(saved_book.reads, 2)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_ctx.pop()


if __name__ == "__main__":
    unittest.main()
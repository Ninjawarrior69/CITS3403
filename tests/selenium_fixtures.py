from app.extensions import db
from app.models import Book, ShelfItem, User

from app.helpers.review_helpers import create_or_update_review


class SeleniumFixturesMixin:
    @classmethod
    def create_user(
        cls,
        name="Selenium User",
        username="seleniumuser",
        email="selenium@example.com",
        password="password123",
        bio="",
        avatar=None,
    ):
        user = User(
            name=name,
            username=username,
            email=email,
            bio=bio,
            avatar=avatar,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def create_book(
        cls,
        title="Selenium Book",
        author="Selenium Author",
        description="Test description",
        page_count=250,
        publish_year=2024,
        cover_url=None,
    ):
        book = Book(
            title=title,
            author=author,
            description=description,
            page_count=page_count,
            publish_year=publish_year,
            cover_url=cover_url,
            rating=0,
            reads=0,
        )
        db.session.add(book)
        db.session.commit()
        return book

    @classmethod
    def add_shelf_item(cls, user, book, status="To Be Read", current_page=0):
        item = ShelfItem(
            user_id=user.id,
            book_id=book.id,
            status=status,
            current_page=current_page,
        )
        db.session.add(item)
        db.session.commit()
        return item

    @classmethod
    def add_review(cls, user, book, stars=5, text="Great read"):
        create_or_update_review(book_id=book.id, stars=stars, text=text, user=user)
        db.session.commit()

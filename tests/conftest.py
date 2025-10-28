import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from app.models import Book, Author, Publisher, Genre


@pytest.fixture(scope="function")
def api_client() -> APIClient:
    yield APIClient()


@pytest.fixture(scope="function")
def admin_user() -> User:
    yield User.objects.create_user(
        username="adminuser",
        password="adminpass123",
        email="adminuser@gmail.com",
        is_staff=True,
    )


@pytest.fixture(scope="function")
def user() -> User:
    yield User.objects.create_user(
        username="testuser",
        password="testpass123",
        email="testuser@gmail.com"
    )


@pytest.fixture(scope="function")
def book() -> Book:
    author = Author.objects.create(name="Test Author")
    publisher = Publisher.objects.create(name="Test Publisher")
    genre = Genre.objects.create(name="Test Genre")

    book = Book.objects.create(
        title='Test Book',
        author=author,
        publisher=publisher,
        genre=genre,
        description='Test Description',
        price=100
    )

    return book


@pytest.fixture(scope="function")
def book_update(book) -> dict:
    return {
        "title": "New Book Title",
        "author": book.author.id,
        "publisher": book.publisher.id,
        "genre": book.genre.id,
        "description": "New Description",
        "price": 150
    }

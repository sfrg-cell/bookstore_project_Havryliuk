import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_get_book_anon(api_client, book) -> None:

    response = api_client.get(f"/books/{book.id}/", format="json")
    assert response.status_code == 200
    assert response.data['title'] == 'Test Book'


@pytest.mark.django_db
def test_get_book_user(api_client, user, book) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': user.username,
            'password': 'testpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    response = api_client.get(f"/books/{book.id}/", format="json")
    assert response.status_code == 200
    assert response.data['title'] == 'Test Book'


@pytest.mark.django_db
def test_get_book_admin_user(api_client, admin_user, book) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': admin_user.username,
            'password': 'adminpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    response = api_client.get(f"/books/{book.id}/", format="json")
    assert response.status_code == 200
    assert response.data['title'] == 'Test Book'


@pytest.mark.django_db
def test_update_book_anon(api_client, book, book_update) -> None:

    response = api_client.put(f"/books/{book.id}/", book_update, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_update_book_user(api_client, user, book, book_update) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': user.username,
            'password': 'testpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    response = api_client.put(f"/books/{book.id}/", book_update, format="json")
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_book_admin_user(api_client, admin_user, book, book_update) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': admin_user.username,
            'password': 'adminpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    response = api_client.put(f"/books/{book.id}/", book_update, format="json")
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_book_admin_user_invalid_token(api_client, admin_user, book, book_update) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': admin_user.username,
            'password': 'adminpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION='Bearer invalidtoken')

    response = api_client.put(f"/books/{book.id}/", book_update, format="json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_book_anon(api_client, book) -> None:

    response = api_client.delete(f"/books/{book.id}/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_delete_book_user(api_client, user, book) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': user.username,
            'password': 'testpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    response = api_client.delete(f"/books/{book.id}/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_book_admin_user(api_client, admin_user, book) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': admin_user.username,
            'password': 'adminpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    response = api_client.delete(f"/books/{book.id}/")
    assert response.status_code == 204


@pytest.mark.django_db
def test_delete_nonexistentbook_admin_user(api_client, admin_user, book) -> None:

    login_url = reverse('token_obtain_pair')
    tokens = api_client.post(
        login_url,
        {
            'username': admin_user.username,
            'password': 'adminpass123',
        },
        format="json"
    ).data

    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

    response = api_client.delete(f"/books/0/")
    assert response.status_code == 404

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

test_cases = [
    ("https://example.com", 200),
    ("invalid-url", 422),
    ("ftp://example.com/file.txt", 200),
]

@pytest.mark.parametrize("url, expected_status", test_cases)
def test_shorten_url(url, expected_status):
   #Тестирование создания коротких ссылок с разными входными данными
    response = client.post("/shorten", json={"url": url})
    assert response.status_code == expected_status

def test_redirect_url():
    #Тестирование перенаправления по короткой ссылке
    # Сначала создаем короткую ссылку
    response = client.post("/shorten", json={"url": "https://example.com"})
    assert response.status_code == 200
    short_url = response.json()["short_url"]
    
    # Затем пробуем перейти по ней
    response = client.get(short_url, follow_redirects=False)
    assert response.status_code in [307, 302]  # redirect

def test_nonexistent_url():
    #Тестирование обработки несуществующей короткой ссылки
    response = client.get("/nonexistent")
    assert response.status_code == 404
"""
Тестирование функций клиента для получения новостей.
"""
import pytest

from clients.news import NewsClient
from settings import API_KEY_NEWSAPI


@pytest.mark.asyncio
class TestCurrencyCountry:
    """
    Тестирование клиента для получения новостей.
    """

    base_url = "https://newsapi.org/v2/everything/"

    @pytest.fixture
    def client(self):
        return NewsClient()

    async def test_get_base_url(self, client):
        assert await client.get_base_url() == self.base_url

    async def test_get_rates(self, mocker, client):
        mocker.patch("clients.news.NewsClient._request")

        await client.get_news("test")
        client._request.assert_called_with(
            f"{self.base_url}?apiKey={API_KEY_NEWSAPI}&pageSize=3&q=test&sortBy=publishedAt"
        )

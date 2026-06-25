# test_client.py — unit tests for DeepLClient
# HTTP calls are mocked — no real API calls made

import pytest
from unittest.mock import MagicMock, patch
from parlez_deepl import DeepLClient


def test_translate_returns_translated_text():
    """Happy path — API returns a valid translation."""
    with patch("parlez_deepl.client.httpx.Client") as mock_http_class:
        # Set up mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "translations": [{"text": "Bonjour"}]
        }
        mock_response.raise_for_status.return_value = None

        # Wire mock into the client
        mock_http_class.return_value.post.return_value = mock_response

        client = DeepLClient(api_key="fake-key")
        result = client.translate("hello", target_lang="FR")

        assert result == "Bonjour"


def test_translate_raises_on_http_error():
    """API returns 4xx/5xx — should raise."""
    with patch("parlez_deepl.client.httpx.Client") as mock_http_class:
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = Exception("403 Forbidden")

        mock_http_class.return_value.post.return_value = mock_response

        client = DeepLClient(api_key="bad-key")

        with pytest.raises(Exception, match="403 Forbidden"):
            client.translate("hello", target_lang="FR")
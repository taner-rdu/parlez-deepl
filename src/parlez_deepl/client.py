# client.py — core SDK logic for calling the DeepL REST API
# Class-based design so callers instantiate once and reuse

import httpx

# DeepL free tier uses api-free.deepl.com, paid uses api.deepl.com
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"


class DeepLClient:
    """Minimal DeepL API client. Instantiate once, reuse for multiple translations."""

    def __init__(self, api_key: str):
        # Store the key and set up a persistent httpx session for connection reuse
        self._api_key = api_key
        self._http = httpx.Client(
            headers={"Authorization": f"DeepL-Auth-Key {api_key}"}
        )

    def translate(self, text: str, target_lang: str) -> str:
        """
        Translate text using the DeepL REST API.

        Args:
            text: The text to translate
            target_lang: Target language code e.g. "FR", "DE", "ES"

        Returns:
            Translated text as a string

        Raises:
            httpx.HTTPStatusError: if the API returns an error response
        """
        payload = {
            "text": [text],
            "target_lang": target_lang,
        }

        response = self._http.post(DEEPL_API_URL, json=payload)

        # Raise an exception if the response is 4xx or 5xx
        response.raise_for_status()

        return response.json()["translations"][0]["text"]

    def close(self):
        """Close the underlying HTTP session."""
        self._http.close()
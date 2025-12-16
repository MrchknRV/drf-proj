import re
from urllib.parse import urlparse

from rest_framework import serializers


def url_validator(value):

    if not value:
        return

    url_pattern = r'(https?://[^\s<>"\'{}|\\^`]+|www\.[^\s<>"\'{}|\\^`]+)'
    urls = re.findall(url_pattern, value, re.IGNORECASE)

    acceptable_domains = (
        "youtube.com",
        "www.youtube.com",
    )

    for url in urls:

        if url.lower().startswith("www."):
            url = "https://" + url
        elif not url.lower().startswith(("http://", "https://")):
            url = "https://" + url

        domain = urlparse(url).netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        if domain not in acceptable_domains:
            raise serializers.ValidationError("В материалах разрешены только ссылки на YouTube.")

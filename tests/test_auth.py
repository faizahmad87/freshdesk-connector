import base64
import os
import pytest

os.environ.setdefault("FRESHDESK_DOMAIN", "testdomain")
os.environ.setdefault("FRESHDESK_API_KEY", "test_api_key_123")

from app.utils.auth import FreshdeskAuth


def test_auth_header_format():
    header = FreshdeskAuth.get_auth_header()
    assert "Authorization" in header
    assert header["Authorization"].startswith("Basic ")


def test_auth_header_encodes_api_key_with_x():
    header = FreshdeskAuth.get_auth_header()
    token = header["Authorization"].replace("Basic ", "")
    decoded = base64.b64decode(token).decode()
    assert decoded == "test_api_key_123:X"

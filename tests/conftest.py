"""Shared pytest fixtures for Estfeed tests."""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import aiohttp
import pytest

pytest_plugins = ["pytest_homeassistant_custom_component"]


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):  # noqa: ARG001
    """Enable loading of custom_components/ in every test."""
    yield


@pytest.fixture(autouse=True)
def aioresponses_stream_writer(monkeypatch: pytest.MonkeyPatch) -> None:
    """Give aioresponses' fake responses the stream_writer aiohttp 3.14 requires.

    aioresponses 0.7.9 builds ClientResponse without it; drop this once it does.
    """
    original = aiohttp.ClientResponse.__init__

    def init(self: aiohttp.ClientResponse, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("stream_writer", SimpleNamespace(output_size=0))
        original(self, *args, **kwargs)

    monkeypatch.setattr(aiohttp.ClientResponse, "__init__", init)

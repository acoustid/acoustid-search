import pytest
from aiohttp.web import Application

from acoustid_search.app import create_app


@pytest.fixture()
def app(loop) -> Application:
    return create_app()

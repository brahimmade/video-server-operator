import pytest
import asyncio

__all__ = [
    'async_loop'
]


@pytest.fixture(scope='session')
def async_loop():
    return asyncio.get_event_loop()

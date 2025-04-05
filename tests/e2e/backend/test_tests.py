import pytest
import asyncio

@pytest.mark.backend
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_tests():
    await asyncio.sleep(10)
    assert True
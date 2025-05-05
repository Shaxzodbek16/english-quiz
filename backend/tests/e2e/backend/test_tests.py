import pytest
import asyncio

@pytest.mark.asyncio
async def test_tests():
    await asyncio.sleep(10)
    assert True

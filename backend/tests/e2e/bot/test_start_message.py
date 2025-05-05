import pytest
import asyncio


@pytest.mark.asyncio
async def test_start_message():
    await asyncio.sleep(10)
    assert True

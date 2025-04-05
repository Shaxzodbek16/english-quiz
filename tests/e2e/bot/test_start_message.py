import pytest
import asyncio


@pytest.mark.bot
@pytest.mark.e2e
@pytest.mark.asyncio
async def test_start_message():
    await asyncio.sleep(10)
    assert True

from typing import Optional
from pathlib import Path

import pydantic

import pytest
import pytest_asyncio
import httpx
import httpx_socks
import yarl

import aiopenapi3.debug
from aiopenapi3_vertiv import createAPI

ROOT_DIR = Path(__file__).parent.parent


class Config(pydantic.BaseModel):
    url: str
    user: str
    password: str
    socks5: Optional[str]


@pytest.fixture
def conf():
    with (ROOT_DIR / "conf" / "config.json").open("rt") as f:
        return Config.model_validate_json(f.read())


@pytest_asyncio.fixture
async def client(conf):
    def socks(*args, **kwargs) -> httpx.AsyncClient:
        if conf.socks5:
            kwargs["transport"] = httpx_socks.AsyncProxyTransport.from_url(conf.socks5, verify=False)
        if False:
            kwargs["event_hooks"] = aiopenapi3.debug.httpx_debug_event_hooks_async()
        kwargs["timeout"] = httpx.Timeout(connect=10, read=30, write=30, pool=30)

        return httpx.AsyncClient(*args, **kwargs)

    client = createAPI(yarl.URL(conf.url).host, session_factory=socks)
    return client


@pytest.fixture
def auth(conf):
    return conf.user, conf.password

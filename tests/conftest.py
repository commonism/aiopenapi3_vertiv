from typing import Optional
from pathlib import Path

import pydantic
from aiopenapi3 import OpenAPI, FileSystemLoader
import aiopenapi3.debug

import pytest
import pytest_asyncio
import httpx
import httpx_socks

ROOT_DIR = Path(__file__).parent.parent
DD = ROOT_DIR / "src/aiopenapi3_vertiv/description_document/openapi.yaml"


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
        kwargs["timeout"] = httpx.Timeout(connect=10, read=30, write=30, pool=30)
        #        kwargs["event_hooks"] = aiopenapi3.debug.httpx_debug_event_hooks_async()
        return httpx.AsyncClient(*args, **kwargs)

    client = OpenAPI.load_file(
        conf.url + "/openapi.yaml", DD.name, session_factory=socks, loader=FileSystemLoader(DD.parent)
    )
    return client


@pytest.fixture
def auth(conf):
    return conf.user, conf.password

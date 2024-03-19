from typing import Optional
from pathlib import Path

import pydantic
from aiopenapi3 import OpenAPI, FileSystemLoader
import aiopenapi3.debug
import json

ROOT_DIR = Path(__file__).parent.parent
DD = ROOT_DIR / "src/aiopenapi3_vertiv/openapi.yaml"

import pytest
import pytest_asyncio
import httpx
import httpx_socks


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
        kwargs["event_hooks"] = aiopenapi3.debug.httpx_debug_event_hooks_async()
        return httpx.AsyncClient(*args, **kwargs)

    client = OpenAPI.load_file(
        conf.url + "/openapi.yaml", DD.name, session_factory=socks, loader=FileSystemLoader(DD.parent)
    )
    return client


@pytest.fixture
def auth():
    return ("cispa", "GreenITCispa")


@pytest.mark.asyncio
async def test_auth(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    assert r.data.root.token
    assert r.retMsg == "Success"

    token = r.data.root.token
    r = await client._.users(data=client._.users.data.get_type()(token=token))
    print(json.dumps(r.model_dump(), indent=4))

    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="logout", token=token, data=dict())
    )


@pytest.mark.asyncio
async def test_sys(client, auth):
    sys = await client._.sys(data=client._.sys.data.get_type()(token=""))
    print(json.dumps(sys.model_dump(), indent=4))

    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    assert r.data.root.token
    token = r.data.root.token

    sys = await client._.sys(data=client._.sys.data.get_type()(token=token))
    print(json.dumps(sys.model_dump(), indent=4))


@pytest.mark.asyncio
async def test_conf(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.root.token

    f = client._.conf
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confNetwork
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confNetworkAddresses
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confNetworkDNS
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confContact
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confSystem
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confReport
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confEmail
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confEmailTarget
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confEmailStatus
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

    f = client._.confSNMP
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))


@pytest.mark.asyncio
async def test_conf_X(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.root.token
    f = client._.confSNMP
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))


@pytest.mark.asyncio
async def test_dev(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.root.token
    r = await client._.dev(data=client._.dev.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))


@pytest.mark.asyncio
async def test_alarm(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.root.token
    r = await client._.alarm(data=client._.alarm.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))


@pytest.mark.asyncio
async def test_sys(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.root.token
    r = await client._.sys(data=client._.sys.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

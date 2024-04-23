import json


import pytest


@pytest.mark.asyncio
async def test_auth(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    assert r.data.token
    assert r.retMsg == "Success"

    token = r.data.token
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
    assert r.data.token
    token = r.data.token

    sys = await client._.sys(data=client._.sys.data.get_type()(token=token))
    print(json.dumps(sys.model_dump(), indent=4))


@pytest.mark.asyncio
async def test_conf(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.token

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
    token = r.data.token
    f = client._.confSNMP
    r = await f(data=f.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))


@pytest.mark.asyncio
async def test_dev(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.token
    r = await client._.dev(data=client._.dev.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))


@pytest.mark.asyncio
async def test_alarm(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.token
    r = await client._.alarm(data=client._.alarm.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))


@pytest.mark.asyncio
async def test_sys(client, auth):
    r = await client._.auth(
        parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
    )
    token = r.data.token
    r = await client._.sys(data=client._.sys.data.get_type()(token=token))
    print(json.dumps(r.model_dump(exclude_unset=True), indent=4, sort_keys=True))

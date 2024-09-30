from pathlib import Path
import json

import pytest

from aiopenapi3_vertiv import createAPI


@pytest.fixture()
def client():
    client = createAPI("127.0.0.1")
    return client


@pytest.fixture()
def DeviceResponse(client):
    req = client.createRequest("dev")
    t = req.operation.responses["200"].content["application/json"].schema_.get_type()
    return t


@pytest.mark.parametrize(
    "device_type",
    [
        pytest.param(i, id=i)
        for i in ["a2d", "afht3", "i03", "remotetemp", "rs", "snd", "snh", "snt", "t3hd", "thd", "vrc"]
    ],
)
def test_response(device_type, DeviceResponse):
    data = json.loads((Path(__file__).parent / "data" / f"{device_type}.json").read_text())

    name = list(data.keys())[0]

    data[name].update(
        {"state": "normal", "snmpInstance": 0, "order": 0, "alarm": {"state": "tripped", "severity": "alarm"}}
    )

    DeviceResponse.model_validate({"retCode": 0, "retMsg": "", "data": data})

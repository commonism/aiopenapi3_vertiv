# aiopenapi3_vertiv

OpenAPI3 description document for geist / Vertiv PDUs

Based on the vendor documents:

  * a78d15c53d702efea2099f8a7d53dffc1a667822  [geist-api-specification-api-specifications-sl-70874.pdf](https://web.archive.org/web/20240901070650/https://www.vertiv.com/4a5036/globalassets/products/critical-power/power-distribution/vertiv-geist-monitored-rack-pdu2/geist-api-specification-api-specifications-sl-70874.pdf)
  * 107682121fea4883a9d6cdd9002497bae060037e  doc/geist-api-guide-2.pdf
  * 332a8c0e8b2ac7a34184fe8888806e456a2ae76d  doc/geist_api_public.pdf
  * 107682121fea4883a9d6cdd9002497bae060037e  doc/geist-vertiv-api-guide-2.pdf

# Examples

## Switching an Outlet

Assuming the outlet is labeled with the machine name.

```python
from aiopenapi3_vertiv import createAPI

def toggle(name):
    if False:  # get the pdus by querying your NetBox DCIM
        dev = next((r := dcim.nb.dcim.devices.filter(name=name)))
        assert len(r) == 1
        pdus = list(dcim.nb.dcim.devices.filter(rack_id=dev.rack.id, position__empty=True, device_role="PDU"))
        assert len(pdus) == 2
        pdus = [pdu.primary_ip for pdu in pdus]
    else:
        pdus = ["192.168.0.1/32","192.168.0.1/32"]

    assert len(pdus) == 2
    clients = [createAPI(ipaddress.ip_network(pdu).network_address) for p in pdus]

    for api in clients:
        # authenticate to the pdu to get the token
        r = api._.auth(
            parameters=dict(user=auth[0]), data=api._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
        )
        assert r.data.token
        assert r.retMsg == "Success"

        token = r.data.token
        r = api._.dev(data=api._.dev.data.get_type()(token=token))

        # i03 is the rPDU unit controlling the outlets
        device, i03 = next(filter(lambda x: x[1].root.type == "i03", r.data.root.items()))

        # filter outlets with label == name
        for oid,outlet in filter(lambda x: x[1].label == name, i03.root.outlet.root.items()):
            print(outlet.name)

            # set mode to manual
            data = api._.outlet.data.get_type().model_validate({'cmd': "set", "token": token, "data": {"mode":"manual"}})
            r = api._.outlet(parameters={"device": device, "outlet": oid}, data=data.model_dump(exclude_unset=True))
            assert r.retCode == 0, r

            # power off
            data = api._.outlet.data.get_type().model_validate({'cmd':"control", "token":token, "data": {"action": "off", "delay": False}}).model_dump()
            r = api._.outlet(parameters={"device":device, "outlet":oid}, data=data)
            assert r.retCode == 0, r

        # wait for things to settle before powering on again
        time.sleep(30)


    for api in clients:
        for oid,outlet in filter(lambda x: x[1].label == name, i03.root.outlet.root.items()):
            print(outlet.name)
            # set mode to "On - if any Alarm Off"
            data = {'cmd': "set", "token": token, "data": {"mode":"alarmAnyOff"}}
            r = api._.outlet(parameters={"device": device, "outlet": oid}, data=data)
            assert r.retCode == 0, r
```

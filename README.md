# aiopenapi3_vertiv

OpenAPI3 description document for geist / Vertiv PDUs

# Examples

## Switching an Outlet

Assuming the outlet is labeled with the machine name.

```python
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
    for pdu in pdus:
        addr = ipaddress.ip_network(pdu).network_address

        client = OpenAPI.load_file(
            f"http://{addr}/openapi.yaml", DD.name, loader=FileSystemLoader(DD.parent)
        )

        # authenticate to the pdu to get the token
        r = client._.auth(
            parameters=dict(user=auth[0]), data=client._.auth.data.get_type()(cmd="login", data={"password": auth[1]})
        )
        assert r.data.token
        assert r.retMsg == "Success"

        token = r.data.token
        r = client._.dev(data=client._.dev.data.get_type()(token=token))

        # i03 is the rPDU unit controlling the outlets
        device, i03 = next(filter(lambda x: x[1].root.type == "i03", r.data.root.items()))

        # filter outlets with label == name
        for oid,outlet in filter(lambda x: x[1].label == name, i03.root.outlet.root.items()):
            print(outlet.name)

            # set mode to manual
            data = client._.outlet.data.get_type().model_validate({'cmd': "set", "token": token, "data": {"mode":"manual"}})
            r = client._.outlet(parameters={"device": device, "outlet": oid}, data=data.model_dump(exclude_unset=True))
            assert r.retCode == 0, r

            # power off
            data = client._.outlet.data.get_type().model_validate({'cmd':"control", "token":token, "data": {"action": "off", "delay": False}}).model_dump()
            r = client._.outlet(parameters={"device":device, "outlet":oid}, data=data)
            assert r.retCode == 0, r

        # wait for things to settle before powering on again
        time.sleep(30)


        for oid,outlet in filter(lambda x: x[1].label == name, i03.root.outlet.root.items()):
            print(outlet.name)
            # set mode to "On - if any Alarm Off"
            data = {'cmd': "set", "token": token, "data": {"mode":"alarmAnyOff"}}
            r = client._.outlet(parameters={"device": device, "outlet": oid}, data=data)
            assert r.retCode == 0, r
```

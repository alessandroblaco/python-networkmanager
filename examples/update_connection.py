"""
Activate a connection by name
"""

import NetworkManager
import sys
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


def merge(source, destination):
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            merge(value, node)
        else:
            destination[key] = value


# Find the connection
name = sys.argv[1]
connections = NetworkManager.Settings.ListConnections()
connections = dict([(x.GetSettings()['connection']['id'], x)
                    for x in connections])
conn = connections[name]
settings = conn.GetSettings()
changes = {"ipv4": {
    "method": "manual",
    "address-data": [{"address": "192.168.1.4", "prefix": 24}]
}}
changes = {"ipv4": {
    "method": "auto",
}}

merge(changes, settings)
conn.Update(settings)
ctype = settings['connection']['type']

dtype = {
    '802-11-wireless': NetworkManager.NM_DEVICE_TYPE_WIFI,
    '802-3-ethernet': NetworkManager.NM_DEVICE_TYPE_ETHERNET,
    'gsm': NetworkManager.NM_DEVICE_TYPE_MODEM,
}.get(ctype, ctype)
devices = NetworkManager.NetworkManager.GetDevices()

for dev in devices:
    if dev.DeviceType == dtype:  # and dev.Interface == interface:
        break

NetworkManager.NetworkManager.ActivateConnection(conn, dev, "/")

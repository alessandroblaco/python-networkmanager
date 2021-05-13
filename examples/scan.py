"""
Show and monitor available access points
"""
from gi.repository import GObject, GLib
import dbus.mainloop.glib
import NetworkManager
import subprocess
from pprint import pprint
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


ssids = {}
device = None

interface = "wlan0"

# cerco l'interfaccia wifi (NetworkManager.Device & NetworkManager.Device.Wireless)
# https://developer.gnome.org/NetworkManager/1.14/gdbus-org.freedesktop.NetworkManager.Device.html#gdbus-property-org-freedesktop-NetworkManager-Device.Interface
# https://developer.gnome.org/NetworkManager/1.14/gdbus-org.freedesktop.NetworkManager.Device.Wireless.html#gdbus-property-org-freedesktop-NetworkManager-Device-Wireless.HwAddress

for dev in NetworkManager.Device.all():
    # è wifi e nome interfaccia (e.g. wlan0) corrisponde
    if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI and dev.Interface == interface:
        device = dev

# Questo comando fa lo scan delle reti disponibili. Ignoro l'output e lo sfrutto solo per triggerare lo scan e per sapere quando è finito
retcode = subprocess.call(["nmcli", "device", "wifi", "list", "ifname", interface],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.STDOUT)

# elenco le reti disponibili

# Qui un esempio di come mostrare il tipo di sicurezza della rete
# https://github.com/NetworkManager/NetworkManager/blob/dc56a21ed6a21565d979887ba9ebc0334e791c47/examples/python/gi/show-wifi-networks.py#L97
for ap in device.GetAllAccessPoints():
    try:
        ssids[ap.object_path] = ap.Ssid
        print("* %-30s %s %sMHz %s%%" %
              (ap.Ssid, ap.HwAddress, ap.Frequency, ap.Strength))
        pprint(ap)
    except NetworkManager.ObjectVanished:
        pass
print(ssids.keys())

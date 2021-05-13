"""
Display all visible SSIDs
"""

import os
import NetworkManager
import dbus.mainloop.glib
import time
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

os.system("nmcli device wifi list")

for dev in NetworkManager.NetworkManager.GetDevices():
    if dev.DeviceType != NetworkManager.NM_DEVICE_TYPE_WIFI:
        continue
#    dev.RequestScan({"ssid": "aay"})
    for ap in dev.GetAccessPoints():
        print('%-30s %dMHz %d%%' %
              (ap.Ssid, ap.Frequency, ap.Strength))
        print(ap.WpaFlags, ap.Flags, ap.RsnFlags,
              time.clock_gettime(time.CLOCK_BOOTTIME) - ap.LastSeen)

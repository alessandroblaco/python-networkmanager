"""
Show and monitor available access points
"""
from gi.repository import GObject, GLib
import dbus.mainloop.glib
import NetworkManager
import time

# Cache the ssids, as the SSid property will be unavailable when an AP
# disappears
ssids = {}
last_seen = 0
last_scan_start = 0
device = None
timeout = 15
finished = False


def main():
    global device
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    # Listen for added and removed access points
    for dev in NetworkManager.Device.all():
        if dev.DeviceType == NetworkManager.NM_DEVICE_TYPE_WIFI:
            # dev.OnAccessPointAdded(ap_added)
            # dev.OnAccessPointRemoved(ap_removed)
            device = dev
    for ap in NetworkManager.AccessPoint.all():
        try:
            ssids[ap.object_path] = ap.Ssid
            print("* %-30s %s %sMHz %s%%" %
                  (ap.Ssid, ap.HwAddress, ap.Frequency, ap.Strength))
            # ap.OnPropertiesChanged(ap_propchange)
        except NetworkManager.ObjectVanished:
            pass
    doScan()
    GLib.timeout_add(30*1000, doScan)
    GLib.MainLoop().run()


def doScan():
    global last_scan_start, last_seen, finished
    finished = False
    print("Scan started")
    last_scan_start = time.clock_gettime(time.CLOCK_BOOTTIME)
    try:
        device.RequestScan({})
        GLib.timeout_add(250, checkFinished)
    except Exception as e:
        print(e)
        print("Skipping scan")
    return True


def checkFinished():
    global finished, last_seen
    for ap in NetworkManager.AccessPoint.all():  # device.GetAccessPoints():
        try:
            if ap.LastSeen > last_scan_start + 0.1 and ((not ap.Ssid in ssids) or not ssids[ap.Ssid] == ap.LastSeen):
                print("* %-30s %s %sMHz %s%%" % (ap.Ssid,
                                                 ap.HwAddress, ap.Frequency, ap.Strength))
                ssids[ap.Ssid] = ap.LastSeen
                last_seen = ap.LastSeen
                finished = True
        except NetworkManager.ObjectVanished:
            pass
    #now = time.clock_gettime(time.CLOCK_BOOTTIME)
    if finished:
        if time.clock_gettime(time.CLOCK_BOOTTIME) - last_seen > 1:
            print("Scan finished {}, {}".format(
                time.clock_gettime(time.CLOCK_BOOTTIME), last_seen))
            return False
        else:
            print("Waiting a little bit more")
            return True
    if time.clock_gettime(time.CLOCK_BOOTTIME) - last_scan_start > timeout:
        print("Scan timeout")
        return False
    return True


def ap_added(dev, interface, signal, access_point):
    global last_seen
    ssids[access_point.object_path] = access_point.Ssid
    print("+ %-30s %s %sMHz %s%%" % (access_point.Ssid,
                                     access_point.HwAddress, access_point.Frequency, access_point.Strength))
    access_point.OnPropertiesChanged(ap_propchange)
    print("{}: Last seen: {}".format(time.time(), access_point.LastSeen))
    last_seen = max(last_seen, access_point.LastSeen)


def ap_removed(dev, interface, signal, access_point):
    print("- %-30s" % ssids.pop(access_point.object_path))


def ap_propchange(ap, interface, signal, properties):
    global last_seen
    if 'Strength' in properties:
        print("  %-30s %s %sMHz %s%%" %
              (ap.Ssid, ap.HwAddress, ap.Frequency, properties['Strength']))
    if 'LastSeen' in properties:
        print("{}: Last seen: {}".format(time.time(), properties['LastSeen']))
        last_seen = max(last_seen, properties['LastSeen'])


if __name__ == '__main__':
    main()

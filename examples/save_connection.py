"""
Activate a connection by name
"""

import NetworkManager
import sys
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

# Find the connection
name = sys.argv[1]
connections = NetworkManager.Settings.ListConnections()
connections = dict([(x.GetSettings()['connection']['id'], x)
                    for x in connections])
conn = connections[name]
conn.Save()

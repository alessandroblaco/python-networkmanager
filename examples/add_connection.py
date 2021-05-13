"""
Add a connection to NetworkManager. You do this by sending a dict to
AddConnection. The dict below was generated with n-m dump on an existing
connection and then anonymised
"""

import subprocess
import NetworkManager
import uuid
import dbus.mainloop.glib
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

ssid = input("SSID: \n")
psk = input("Password: \n")
name = input("Nome: \n")

# as in https://github.com/NetworkManager/NetworkManager/blob/dc56a21ed6a21565d979887ba9ebc0334e791c47/examples/python/dbus/add-wifi-psk-connection.py
example_connection = {
    '802-11-wireless': {'mode': 'infrastructure',
                        'security': '802-11-wireless-security',
                        'ssid': ssid},
    # https://developer.gnome.org/NetworkManager/1.14/settings-802-11-wireless-security.html
    '802-11-wireless-security': {'auth-alg': 'open', 'key-mgmt': 'wpa-psk', 'psk': psk},
    'connection': {'id': name,
                   'type': '802-11-wireless',
                   'uuid': str(uuid.uuid4())},
    'ipv4': {'method': 'auto'},
    'ipv6': {'method': 'ignore'}
}

NetworkManager.Settings.AddConnectionUnsaved(example_connection)


p = subprocess.Popen(
    ["nmcli", "con", "up", name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

output, error = p.communicate()
output = output.decode("utf-8")

print(output)

connections = NetworkManager.Settings.ListConnections()
connections = dict([(x.GetSettings()['connection']['id'], x)
                    for x in connections])
conn = connections[name]
if output.find("success") > 0:
    print("Connection successful, saving")
    conn.Save()
else:
    print("Connection failed, deleting")
    conn.Delete()

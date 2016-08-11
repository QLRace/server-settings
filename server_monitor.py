#!/usr/bin/env python2
import valve.source.a2s as a2s
import os
import sys
import socket
import time
import supervisor.xmlrpc
import xmlrpclib

supervisor_socket = "unix:///tmp/supervisor.sock"

try:
    location = os.environ["LOCATION"]
    if location not in ("DE", "IL", "AU", "NL"):
        raise KeyError
except KeyError:
    print("Invalid LOCATION env value.")
    sys.exit()

if location == "DE":
    SERVERS = {27960: "turbo1", 27961: "turbo2", 27962: "turbo3", 27963: "turbo4",
               27970: "classic1", 27971: "classic2", 27972: "classic3", 27973: "classic4"}
elif location == "IL":
    SERVERS = {27960: "turbo1", 27961: "turbo2", 27962: "turbo3", 27970: "classic1", 27971: "classic2"}
elif location == "AU":
    SERVERS = {27960: "turbo1", 27961: "turbo2", 27970: "classic1", 27971: "classic2"}
else:
    SERVERS = {27960: "turbo", 27961: "classic"}


def main():
    offline = []
    for port, name in sorted(SERVERS.items()):
        info = get_server_info(port)
        if info:
            players = "{player_count}/{max_players}".format(**info)
            print("{} (localhost:{}) is running {}".format(name, port, players))
        else:
            offline.append(port)
            print("{} (localhost:{}) is offline. Will check again in 20 seconds.".format(name, port))

    if offline:
        time.sleep(20)
        for port in offline:
            info = get_server_info(port)
            if info:
                players = "{player_count}/{max_players}".format(**info)
                print("{} (localhost:{}) is now running {}".format(SERVERS[port], port, players))
            else:
                print("{} (localhost:{}) is still offline. Restarting...".format(SERVERS[port], port))
                group = SERVERS[port].rstrip("0123456789")
                restart("{}:qzeroded_{}".format(group, SERVERS[port]))


def get_server_info(port):
    try:
        return a2s.ServerQuerier(("localhost", port), 1).get_info()
    except a2s.NoResponseError:
        return


def restart(process_name):
    try:
        transport = supervisor.xmlrpc.SupervisorTransport(serverurl=supervisor_socket)
        server = xmlrpclib.ServerProxy("http://127.0.0.1", transport=transport)
        if server.supervisor.getProcessInfo(process_name)["statename"] != "STOPPED":
            server.supervisor.stopProcess(process_name)
            server.supervisor.startProcess(process_name)
            print("{} was restarted!".format(process_name))
        else:
            print("{} is stopped so not restarting.".format(process_name))
    except socket.error:
        print("Error connection to supervisor.")
    except xmlrpclib.Fault:
        print("Invalid process name({}).".format(process_name))


if __name__ == "__main__":
    main()

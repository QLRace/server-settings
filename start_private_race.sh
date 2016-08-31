#!/bin/bash
cd ~/qlds/baseq3 || exit 1
source private.sh || exit 1

if [[ $1 == "turbo" ]]; then
    mode=0
    gamePort=27960
    rconPort=28960
    mapPool="mappool_qlrace.txt"
    hostname="QLRace.com Private - Turbo (PQL)"
elif [[ $1 == "classic" ]]; then
    mode=2
    gamePort=27961
    rconPort=28961
    mapPool="mappool_qlrace_classic.txt"
    hostname="QLRace.com Private - Classic (VQL)"
else
    exit 1
fi

exec /home/steam/qlds/run_server_x64_minqlx.sh \
    +set com_hunkmegs 44 \
    +set fs_homepath /home/steam/.quakelive/$gamePort \
    +set g_password $PRIVATE_PW \
    +set net_port $gamePort \
    +set sv_hostname $hostname \
    +set sv_mappoolFile $mapPool \
    +set sv_maxclients 12 \
    +set zmq_rcon_enable 1 \
    +set zmq_rcon_password $RCON_PW \
    +set zmq_rcon_port $rconPort \
    +set zmq_stats_enable 1 \
    +set zmq_stats_password $STATS_PW \
    +set qlx_cleverBotKey $CB_KEY \
    +set qlx_cleverBotUser $CB_USER \
    +set qlx_raceKey $RACE_KEY \
    +set qlx_raceMode $mode \
    +set qlx_servers "nl.qlrace.com:27960, nl.qlrace.com:27961, de.qlrace.com:27960, de.qlrace.com:27961, de.qlrace.com:27962, de.qlrace.com:27963, de.qlrace.com:27970, de.qlrace.com:27971, de.qlrace.com:27972, de.qlrace.com:27973, il.qlrace.com:27960, il.qlrace.com:27961, il.qlrace.com:27962, il.qlrace.com:27970, il.qlrace.com:27971, au.qlrace.com:27960, au.qlrace.com:27961, au.qlrace.com:27970, au.qlrace.com:27971"

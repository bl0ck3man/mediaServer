#!/bin/bash

mkdir -p /var/run/dbus
rm -f /var/run/dbus/pid
service dbus start
avahi-daemon -D

exec netatalk -d
#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pyzabbix import ZabbixAPI
zapi = ZabbixAPI("http://192.168.61.14:8542")
zapi.login("Admin", "zabbix")


for h in zapi.host.get(output="extend"):
    print(h['hostid'])

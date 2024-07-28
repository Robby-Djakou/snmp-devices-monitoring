printf '
###############################################################################
#                            OUTPUT PLUGINS                                   #
###############################################################################


# Configuration for sending metrics to InfluxDB
[[outputs.influxdb]]
  urls = ["http://127.0.0.1:8086"]
  database = "telegraf"

  ## HTTP Basic Auth
  username = "telegraf"
  password = "telegraf"

[[inputs.snmp]]
  agents = ["udp://%s:161"]
  timeout = "5s"
  sec_name = "%s"
  auth_protocol = "%s"
  auth_password = "%s"
  sec_level = "%s"
  priv_protocol = "%s"
  priv_password = "%s"
  community = "public"
  name = "snmp"
  version = 3
  [[inputs.snmp.field]]
    name = "uptime"
    oid = ".1.3.6.1.2.1.1.3.0"
  [[inputs.snmp.field]]
    name = "gebaeude"
    oid = ".1.3.6.1.2.1.1.5.0"

[[inputs.snmp.table]]
  name = "DATA"
  inherit_tags = [ "source" ]
  [[inputs.snmp.table.field]]
    name = "ifName"
    oid = ".1.3.6.1.2.1.31.1.1.1.1"
    is_tag = true
  [[inputs.snmp.table.field]]
    name = "ifHCInOctets"
    oid = ".1.3.6.1.2.1.31.1.1.1.6"
  [[inputs.snmp.table.field]]
    name = "ifHCOutOctets"
    oid = ".1.3.6.1.2.1.31.1.1.1.10"
  [[inputs.snmp.table.field]]
    name = "ifInDiscards"
    oid = ".1.3.6.1.2.1.2.2.1.13"
  [[inputs.snmp.table.field]]
    name = "ifOutDiscards"
    oid = ".1.3.6.1.2.1.2.2.1.19"
  [[inputs.snmp.table.field]]
    name = "ifInErrors"
    oid = ".1.3.6.1.2.1.2.2.1.14"
  [[inputs.snmp.table.field]]
    name = "ifOutErrors"
    oid = ".1.3.6.1.2.1.2.2.1.20"
  [[inputs.snmp.table.field]]
    name = "ifInUnknownProtos"
    oid = ".1.3.6.1.2.1.2.2.1.15"
  [[inputs.snmp.table.field]]
    name = "ifAlias"
    oid = ".1.3.6.1.2.1.31.1.1.1.18"
    is_tag = true
  [[inputs.snmp.table.field]]
    name = "ifHighSpeed"
    oid = ".1.3.6.1.2.1.31.1.1.1.15"
  [[inputs.snmp.table.field]]
    name = "ifAdminStatus"
    oid = ".1.3.6.1.2.1.2.2.1.7"
    is_tag = true
  [[inputs.snmp.table.field]]
    name = "ifOperStatus"
    oid = ".1.3.6.1.2.1.2.2.1.8"
    
[[inputs.ping]]
  urls = ["%s"] 
  count = 1
  ping_interval = 1.0
  timeout = 1.0
	
' "$1" "$2" "$4" "$5" "$3" "$6" "$7" "$1" >>/etc/telegraf/telegraf.conf

sudo service telegraf stop
sudo service telegraf start
sudo service telegraf restart

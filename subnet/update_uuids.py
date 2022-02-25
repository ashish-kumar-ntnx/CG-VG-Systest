from tinydb import TinyDB, Query
import requests
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass

AUTH = ("admin", "Nutanix.123")
PC_IP = "10.45.72.242"
DB = TinyDB("../db/subnet.json")
subnet_names = ["vlan0"]

url = "https://{0}:9440/api/nutanix/v3/subnets/list".format(PC_IP)
r = requests.post(url, auth=AUTH, json={}, verify=False)
out = r.json()
for i in out["entities"]:
  name = i["status"]["name"]
  if name not in subnet_names:
    continue
  uuid = i["metadata"]["uuid"]
  cluster_name = i["status"]["cluster_reference"]["name"]
  cluster_uuid = i["status"]["cluster_reference"]["uuid"]
  print "Name: {0}, UUID: {1}".format(name, uuid)
  DB.insert({"name": name, "uuid": uuid, "cluster_name": cluster_name, "cluster_uuid": cluster_uuid})

print DB.all()


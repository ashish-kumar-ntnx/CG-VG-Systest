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
DB = TinyDB("../db/ctr.json")
subnet_names = ["vlan0"]

url = "https://{0}:9440/api/nutanix/v3/groups".format(PC_IP)
body = {"entity_type":"storage_container","group_member_attributes":[{"attribute":"container_name"},{"attribute":"cluster_name"},{"attribute":"cluster"}]}
r = requests.post(url, auth=AUTH, json=body, verify=False)
out = r.json()
for i in out["group_results"][0]["entity_results"]:
  name = i["data"][0]["values"][0]["values"][0]
  cluster_name = i["data"][1]["values"][0]["values"][0]
  cluster_uuid = i["data"][2]["values"][0]["values"][0]
  uuid = i["entity_id"]
  #if name not in subnet_names:
  #  continue
  print "Name: {0}, UUID: {1}".format(name, uuid)
  DB.insert({"name": name, "uuid": uuid, "cluster_name": cluster_name, "cluster_uuid": cluster_uuid})

print DB.all()


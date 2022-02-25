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
DB = TinyDB("../db/cluster.json")
cluster_names = ["PC-A-PE-1", "PC-A-PE-2"]

url = "https://{0}:9440/api/nutanix/v3/clusters/list".format(PC_IP)
r = requests.post(url, auth=AUTH, json={}, verify=False)
out = r.json()
for i in out["entities"]:
  name = i["status"]["name"]
  uuid = i["metadata"]["uuid"]
  if name not in cluster_names:
    continue
  print "Name: {0}, UUID: {1}".format(name, uuid)
  DB.insert({"name": name, "uuid": uuid})

print DB.all()


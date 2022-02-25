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
DB = TinyDB("../db/cg.json")

url = "https://{0}:9440/api/dataprotection/v4.0.a1/config/consistency-groups".format(PC_IP)

cg_name_list = ["cg-" + str(i) for i in range(1, 21)]
r = requests.get(url, auth=AUTH, verify=False)
out = r.json()

for cg in out["data"]:
  cg_name = cg["name"]
  if cg_name not in cg_name_list:
    continue
  cg_id = cg["extId"]
  DB.insert({"name": cg_name, "uuid": cg_id})

print DB.all()


import time
import requests
from tinydb import TinyDB, Query
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass

DB = TinyDB("../db/category.json")
AUTH = ("admin", "Nutanix.123")
PC_IP = "10.45.72.242"
count = 22

url = "https://{0}:9440/api/prism/v2.a1/config/categories".format(PC_IP)

for i in range(count):
  k = "cat-" + str(i + 1)
  v = "val-" + str(i + 1)
  body = {"name": k}
  r = requests.post(url, auth=AUTH, json=body, verify=False)
  out = r.json()
  extid = out["data"]["extId"]
  body = {"name": v, "parentExtId": extid}
  r = requests.post(url, auth=AUTH, json=body, verify=False)
  out = r.json()
  extid = out["data"]["extId"]
  print "For category {0}:{1}, extId: {2}".format(k, v, extid)
  DB.insert({"cat_key": k, "cat_val": v, "uuid": extid})

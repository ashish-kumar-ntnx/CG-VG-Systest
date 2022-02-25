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
DB = TinyDB("../db/image.json")

image_names = ["centos_72", "oel_77", "rhel_68", "rhel_72", "rhel_74", "rhel_77", "sles12_sp4", "win2012r2_server", "win2019_server", "oel_69", "rhel_67", "rhel_69", "rhel_73", "rhel_76", "sles11_sp4", "win2008r2_server", "win2016_server"]

url = "https://{0}:9440/api/nutanix/v3/images/list".format(PC_IP)
#fil = "name==" + "|".join(image_names)
filter_criteria = {"filter": "name==" + "|".join(image_names)}
r = requests.post(url, auth=AUTH, json=filter_criteria, verify=False)
out = r.json()
image_name_uuid_map = dict()
for i in out["entities"]:
  name = i["status"]["name"]
  uuid = i["metadata"]["uuid"]
  image_name_uuid_map[name] = uuid
  DB.insert({"name": name, "uuid": uuid})

print image_name_uuid_map
print DB.all()


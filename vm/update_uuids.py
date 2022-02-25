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
DB = TinyDB("../db/vm.json")

url = "https://{0}:9440/api/nutanix/v3/vms/list".format(PC_IP)
#fil = "name==" + "|".join(image_names)
vm_num = 0
for i in range(1, 201, 20):
  name_list = list()
  for j in range(20):
    vm_num += 1
    vm_name = "vm-" + str(vm_num)
    name_list.append(vm_name)
  filter_criteria = {"filter": "vm_name==" + "|".join(name_list)}
  r = requests.post(url, auth=AUTH, json=filter_criteria, verify=False)
  print url, filter_criteria
  out = r.json()
  print out
  for i in out["entities"]:
    name = i["status"]["name"]
    uuid = i["metadata"]["uuid"]
    DB.insert({"name": name, "uuid": uuid})

print DB.all()


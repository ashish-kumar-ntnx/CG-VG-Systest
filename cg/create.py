from tinydb import TinyDB, Query
import time
import requests
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass


BATCH = 10
PC_IP = "10.45.72.242"
AUTH = ("admin", "Nutanix.123")
vm_db = TinyDB("../db/vm.json")
vg_db = TinyDB("../db/vg.json")

def create_cg():
  vm_num = 1
  for i in range(1, 21):
    cg_name = "cg-" + str(i)
    vm_list = []
    vg_list = []

    for i in range(10):
      vm_name = "vm-" + str(vm_num)
      vg_a_name = "vg-a-" + str(vm_num)
      vg_b_name = "vg-b-" + str(vm_num)
      vm_num += 1

      q = Query()
      vm_list.append(vm_db.search(q.name == vm_name)[0]["uuid"])
      q = Query()
      vg_list.append(vg_db.search(q.name == vg_a_name)[0]["uuid"])
      vg_list.append(vg_db.search(q.name == vg_b_name)[0]["uuid"])

    cg_spec = dict()
    cg_spec["name"] = cg_name
    cg_spec["members"] = list()

    for vm in vm_list:
      tmp = dict()
      tmp["entityType"] = "VM"
      tmp["extId"] = vm
      cg_spec["members"].append(tmp)

    for vg in vg_list:
      tmp = dict()
      tmp["entityType"] = "VOLUME_GROUP"
      tmp["extId"] = vg
      cg_spec["members"].append(tmp)

    print "Creating CG: {0} ...".format(cg_name)
    url = "https://{0}:9440/api/dataprotection/v4.0.a1/config/consistency-groups".format(PC_IP)
    r = requests.post(url, auth=AUTH, json=cg_spec, verify=False)
    out = r.json()
    print out

if __name__=="__main__":
  create_cg()

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
cg_db = TinyDB("../db/cg.json")

def update_cg():
  vm_num = 1
  vg_num_a = 1
  vg_num_b = 1
  for i in range(1, 21):
    cg_name = "cg-" + str(i)
    vm_list = []
    vg_list = []

    vm_name_list, vg_name_list = [], []

    for _ in range(10):
      vm_name = "vm-" + str(vm_num)
      vm_num += 1
      q = Query()
      vm_list.append(vm_db.search(q.name == vm_name)[0]["uuid"])
      vm_name_list.append(vm_name)

    if i <= 10:
      vg_prefix = "vg-a-"
      for _ in range(10):
        vg_name_1 = vg_prefix + str(vg_num_a)
        vg_name_2 = vg_prefix + str(vg_num_a + 100)
        vg_name_list.append(vg_name_1)
        vg_name_list.append(vg_name_2)
        vg_num_a += 1
        q = Query()
        vg_list.append(vg_db.search(q.name == vg_name_1)[0]["uuid"])
        vg_list.append(vg_db.search(q.name == vg_name_2)[0]["uuid"])
    else:
      vg_prefix = "vg-b-"
      for _ in range(10):
        vg_name_1 = vg_prefix + str(vg_num_b)
        vg_name_2 = vg_prefix + str(vg_num_b + 100)
        vg_name_list.append(vg_name_1)
        vg_name_list.append(vg_name_2)
        vg_num_b += 1
        q = Query()
        vg_list.append(vg_db.search(q.name == vg_name_1)[0]["uuid"])
        vg_list.append(vg_db.search(q.name == vg_name_2)[0]["uuid"])


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

    print cg_name
    print vm_name_list, vg_name_list
    q = Query()
    cg_uuid = cg_db.search(q.name == cg_name)[0]["uuid"]
    cg_spec["extId"] = cg_uuid
    print "Updating CG: {0} ...".format(cg_name)
    url = "https://{0}:9440/api/dataprotection/v4.0.a1/config/consistency-groups/{1}".format(PC_IP, cg_uuid)
    #print url, cg_spec
    r = requests.put(url, auth=AUTH, json=cg_spec, verify=False)
    out = r.json()
    print out["metadata"]["flags"][0]["name"], out["metadata"]["flags"][0]["value"]

if __name__=="__main__":
  update_cg()

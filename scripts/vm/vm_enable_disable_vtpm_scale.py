from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
from framework.cluster_entity import Cluster
import time
import threading

IP = SRC_PC_IP
CLUS_LIST = SRC_CLUS_LIST
#IP = TGT_PC_IP
#CLUS_LIST = TGT_CLUS_LIST
VM_PREFIX = "vm-scale-"

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()

START = 1
END = 1001
VTPM_ENABLE = False

def update_vm(vm_name):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  vm_spec = v1.get_json()
  vm_spec.pop("status")
  #if vm_spec["spec"].get("vtpm_config", {}).get("vtpm_enabled", False):
  #  return
  print "For VM: {0} setting vtpm: {1}".format(vm_name, VTPM_ENABLE)
  vm_spec["spec"]["resources"]["vtpm_config"] = {"vtpm_enabled": VTPM_ENABLE}
  #print vm_spec
  try:
    v1.update(vm_spec)
  except:
    pass

#for i in range(START, END):
#  vm_name = VM_PREFIX + str(i)
#  update_vm(vm_name)

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = VM_PREFIX + str(j)
    print vm_name
    x = threading.Thread(target=update_vm, args=(vm_name,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()


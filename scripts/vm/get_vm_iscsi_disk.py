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
VM_PREFIX = "vm-"

#IP = SRC_PC_IP
#CLUS_LIST = SRC_CLUS_LIST
#VM_PREFIX = "Nutanix-Test-vm-"

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()

DISK_LENGTH = 21
START = 1
END = 101

def check_disk_count(vm_name):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  len_disks = len(v1.get_sd_disk_list().split(" "))
  print "IQN: {0}".format(v1.get_iqn())
  print "{0}, {1} Disks\n".format(vm_name, len_disks)
  if len_disks != DISK_LENGTH:
    print "IQN: {0}".format(v1.get_iqn())
    print "{0}, {1} Disks\n".format(vm_name, len_disks)
    print "ALERT!!!! VM: {0}".format(vm_name)

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = VM_PREFIX + str(j)
    x = threading.Thread(target=check_disk_count, args=(vm_name,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

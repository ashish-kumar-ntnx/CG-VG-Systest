import sys
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time

IP = TGT_PC_IP
CLUS_LIST = TGT_CLUS_LIST
#IP = SRC_PC_IP
#CLUS_LIST = SRC_CLUS_LIST

vm_obj = VM(IP)

#vm_name_uuid_map = vm_obj.get_name_uuid_map()

vm_name = sys.argv[1]

cluster_name = CLUS_LIST[0]

#if int(vm_name.split("-")[1]) < 101:
#  cluster_name = CLUS_LIST[0]
#else:
#  pass
#  cluster_name = CLUS_LIST[1]


vm = vm_obj.get(vm_name=vm_name, cluster_name=cluster_name)
print "Enabling vdbench on VM: {0} - {1}".format(vm_name, vm.uuid)
vm.enable_vdbench()
"""
vm_list = []
for i in range(0, 200, 10):
  for j in range(1, 4):
    vm_list.append("vm-" + str(i + j))
print vm_list

for vm_name in vm_list:
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  v1.enable_vdbench()
  

START=1
END=11
for i in range(START, END):
  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  v1.enable_vdbench()

START=101
END=111
for i in range(START, END):
  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  v1.enable_vdbench()
"""

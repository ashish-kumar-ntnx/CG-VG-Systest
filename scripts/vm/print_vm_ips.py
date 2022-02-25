from framework.vm_entity import VM
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time

vm_obj = VM(SRC_PC_IP)

#vm_name_uuid_map = vm_obj.get_name_uuid_map()


START=1
END=11
for i in range(START, END):
  cluster_name = "PC-A-PE-1"
  vm_name = "vm-" + str(i)
  #vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_name=vm_name, cluster_name=cluster_name)
  print "VM: {0} - {1}, IP: {2}\n".format(vm_name, v1.uuid, v1.get_vm_ip())

START=101
END=111
for i in range(START, END):
  cluster_name = "PC-A-PE-2"
  vm_name = "vm-" + str(i)
  #vm_uuid = vm_name_uuid_map[vm_name]
  #v1 = vm_obj.get(vm_uuid)
  v1 = vm_obj.get(vm_name=vm_name, cluster_name=cluster_name)
  print "VM: {0} - {1}, IP: {2}\n".format(vm_name, v1.uuid, v1.get_vm_ip())

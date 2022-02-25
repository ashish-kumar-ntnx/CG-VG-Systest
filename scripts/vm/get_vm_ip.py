from framework.vm_entity import VM
from framework.cluster_entity import Cluster
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time

IP = SRC_PC_IP
#IP = TGT_PC_IP
#CLUS_LIST = TGT_CLUS_LIST

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
START = 101
END = 102

vm_ip_list = list()
for i in range(START, END):
  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  vm = vm_obj.get(vm_uuid=vm_uuid)
  vm_ip = vm.get_vm_ip()
  print "VM: {0}, IP: {1}".format(vm_name, vm_ip)
  vm_ip_list.append(vm_ip)

print " ".join(vm_ip_list)

#from framework.vm_entity import VM
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time

IP = SRC_PC_IP
#IP = TGT_PC_IP
vm_obj = VM(IP)
vm_obj = VM(IP)

vm_name_uuid_map = vm_obj.get_name_uuid_map()

GATEWAY = "10.45.128.1"
PREFIX = 17
START=1
END=101
for i in range(START, END):
  vm_name = "vm-" + str(i)
  #if vm_name not in vm_list:
  #  continue
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  vm_ip = v1.get_vm_ip()
  print "Setting static ip on VM: {0}".format(vm_name)
  cmd = "sudo nmcli con mod eth0 ipv4.addresses {0}/{1} ipv4.gateway {2} ipv4.method manual".format(vm_ip, PREFIX, GATEWAY)
  _, out = v1.execute(cmd)
  print out

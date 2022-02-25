from framework.vm_entity import VM
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time

vm_obj = VM(SRC_PC_IP)


vm_name_uuid_map = vm_obj.get_name_uuid_map()


for i in range(1, 201):
  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  print "\n#### VM: {0}, {1} running FIO ####".format(vm_name, vm_uuid)
  v1 = vm_obj.get(vm_uuid)
  v1.trigger_fio()

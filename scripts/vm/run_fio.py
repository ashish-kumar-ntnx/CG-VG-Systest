from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time

vm_obj = VM(SRC_PC_IP)


vm_name_uuid_map = vm_obj.get_name_uuid_map()


for i in range(1, 101):
  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  print "\n#### VM: {0}, {1} running FIO ####".format(vm_name, vm_uuid)
  v1 = vm_obj.get(vm_uuid)
  v1.trigger_fio()

from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM

IP = TGT_PC_IP
IP = SRC_PC_IP

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()

START = 1
END = 161

for i in range(START, END):
  vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(i).rjust(4, '0')
  if vm_name not in vm_name_uuid_map:
    continue
  vm_uuid = vm_name_uuid_map[vm_name]
  vm = vm_obj.get(vm_uuid=vm_uuid)
  print "Removing categories from VM: {0} - {1}".format(vm_name, vm_uuid)
  #print dir(vm)
  vm.remove_category()

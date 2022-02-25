from framework.cg_entity import CG
#from framework.vm_entity import VM
from framework.vg_entity import VG
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM

IP = TGT_PC_IP
IP = SRC_PC_IP
cg = CG(IP)
vm = VM(IP)
vg = VG(IP)

vm_name_list = ["test-vm-1"]
vg_name_list = ["test-vg-1"]
cg_name = "test-cg-1"

vm_name_uuid_map = vm.get_name_uuid_map()
vg_name_uuid_map = vg.get_name_uuid_map()

vm_uuid_list = [vm_name_uuid_map[vm_name] for vm_name in vm_name_list]
vg_uuid_list = [vg_name_uuid_map[vg_name] for vg_name in vg_name_list]

print "Creating CG: {0}, with vms: {1}, vgs: {2}".format(cg_name, vm_name_list, vg_name_list)
cg.create(cg_name, vm_uuid_list, vg_uuid_list)

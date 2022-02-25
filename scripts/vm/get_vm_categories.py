from framework.vm_entity import VM
from framework.image_entity import Image
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM

IP = TGT_PC_IP
#IP = SRC_PC_IP
vm_prefix = "vm-"
#vm_prefix = "Nutanix-Test-vm-"

START = 1
END = 101
vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
no_category_vm_map = dict()

for i in range(START, END):
  vm_name = vm_prefix + str(i)
  if vm_name not in vm_name_uuid_map:
    continue
  vm_uuid = vm_name_uuid_map[vm_name]
  v = vm_obj.get(vm_uuid=vm_uuid)
  cat_on_vm = v.get_categories()
  if not cat_on_vm:
    print "VM: {0} - {1}, No categories attached to this VM".format(vm_name, vm_uuid)
    no_category_vm_map[vm_name] = vm_uuid
  else:
    print "VM: {0} - {1}, Categories: {2}".format(vm_name, vm_uuid, v.get_categories())

print "VMs that have no category"
print no_category_vm_map

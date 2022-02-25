import sys
from framework.vm_entity import VM
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#IP = TGT_PC_IP
IP = SRC_PC_IP

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
cat_obj = Category(IP)

if len(sys.argv) != 6:
  print "\n\tUsage: python add_category_to_single_vm.py <vm_prefix> <vm_start> <vm_end> <cat_key> <cat_val>\n"
  sys.exit(1)
vm_pre = sys.argv[1]
vm_start = int(sys.argv[2])
vm_end = int(sys.argv[3])
cat_key = sys.argv[4]
cat_val = sys.argv[5]


for i in range(vm_start, vm_end):
  vm_name = vm_pre + str(i)
  vm = vm_obj.get(vm_uuid=vm_name_uuid_map[vm_name])
  print "VM: {0} - {1} adding category: ({2}, {3})".format(vm_name, vm.uuid, cat_key, cat_val)
  vm.attach_category(cat_key=cat_key, cat_val=cat_val)

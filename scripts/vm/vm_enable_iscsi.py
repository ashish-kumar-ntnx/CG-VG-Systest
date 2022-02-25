from framework.vm_entity import VM
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

START = 1
END = 101
vm_obj = VM(SRC_PC_IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
#vm_exclude_list = ["vm-" + str(i) for i in range(151, 166)]

for i in range(START, END):
  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  #if vm_name in vm_exclude_list:
  #  continue
  cluster_name = "PC-A-PE-1" if i <= 100 else "PC-A-PE-2"
  print "\n#### VM: {0} ####".format(vm_name)
  v = vm_obj.get(vm_uuid=vm_uuid)
  #v = vm_obj.get(vm_name=vm_name, cluster_name=cluster_name)
  v.enable_iscsi()
  print "Old IQN: {0}".format(v.get_iqn())
  v.generate_new_iqn()
  print "New IQN: {0}".format(v.iqn)

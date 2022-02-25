from framework.vm_entity import VM
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time

START = 1
END = 201

vm_obj = VM(SRC_PC_IP)
vg_obj = VG(SRC_PC_IP)

#vm_exclude_list = ["vm-" + str(i) for i in range(151, 166)] + ["vm-" + str(i) for i in range(1, 63)]

task_map = dict()


vm_name_uuid_map = vm_obj.get_name_uuid_map()
vg_name_uuid_map = vg_obj.get_name_uuid_map()

for i in range(101, 201):
  if i < 101:
    vg_name_1 = "vg-a-" + str(i)
    vg_name_2 = "vg-a-" + str(i + 100)
  else:
    vg_name_1 = "vg-b-" + str(i - 100)
    vg_name_2 = "vg-b-" + str(i)
    
  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]

  print "\n#### VM: {0}, {1} ####\n".format(vm_name, vm_uuid)
  v = vm_obj.get(vm_uuid=vm_uuid)
  iqn = v.get_iqn()
  #iqn = v.generate_new_iqn()

  for vg_name in [vg_name_1, vg_name_2]:
    vg = vg_obj.get(vg_uuid=vg_name_uuid_map[vg_name]) 
    print "Attaching VG: {0}, {1}, iscsiTarget: {2}".format(vg_name, vg.uuid, vg.iscsi_target)
    attach_spec = {"iscsiInitiatorName": iqn}
    task_url = vg.attach_iscsi(attach_spec)
    task_map[vg_name] = {"vm_name": vm_name, "task_url": task_url}

print task_map 

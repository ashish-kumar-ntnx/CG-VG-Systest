from framework.vm_entity import VM
from framework.image_entity import Image
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

START = 78
END = 201
vm_obj = VM(SRC_PC_IP)
image_obj = Image(SRC_PC_IP)
image_name = "centos_72"
i = image_obj.get(image_name=image_name)
image_uuid = i.uuid
image_ref = {"data_source_reference": {"kind": "image", "uuid": image_uuid, "name": image_name}}
vm_exclude_list = ["vm-" + str(i) for i in range(151, 166)]

task_map = dict()
for i in range(START, END):
  vm_name = "vm-" + str(i)
  if vm_name in vm_exclude_list:
    continue
  cluster_name = "PC-A-PE-1" if i <= 100 else "PC-A-PE-2"
  v = vm_obj.get(vm_name=vm_name, cluster_name=cluster_name)
  vm_spec = v.spec
  vm_spec.pop("status")
  vm_spec["spec"]["resources"]["disk_list"][1] = image_ref
  print "Updating VM: {0}".format(vm_name)
  task = v.update(vm_spec) 
  task_map[vm_name] = task
  
print task_map 

from framework.vm_entity import VM
from framework.image_entity import Image
from framework.ctr_entity import Ctr
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time

START = 1
END = 201

vm_obj = VM(SRC_PC_IP)
image_obj = Image(SRC_PC_IP)
ctr_obj = Ctr(SRC_PC_IP)

image_name = "centos_72"
i = image_obj.get(image_name=image_name)
image_uuid = i.uuid
image_ref = {"data_source_reference": {"kind": "image", "uuid": image_uuid, "name": image_name}}
cdrom_ref = {"device_properties":{"disk_address":{"device_index":0,"adapter_type":"SATA"},"device_type":"CDROM"}}
ctr_ref = {"storage_config":{"storage_container_reference":{"kind":"storage_container","uuid":"ad0780b8-035e-4de4-b926-3e60653a303f"}},"device_properties":{"device_type":"DISK","disk_address":{"device_index":1,"adapter_type":"SCSI"}},"disk_size_bytes":5368709120}

vm_exclude_list = ["vm-" + str(i) for i in range(151, 166)] + ["vm-" + str(i) for i in range(1, 63)]

ctr_name_uuid_map = ctr_obj.get_name_uuid_map()

task_map = dict()

vm_num = 1
ctr_num = 1

for i in range(1, 201, 10):
  ctr_name = "cg-vg-ctr-" + str(ctr_num)
  ctr_num += 1
  ctr_uuid = ctr_name_uuid_map[ctr_name]
  for j in range(10):
    vm_name = "vm-" + str(vm_num)
    vm_num += 1
    if vm_name in vm_exclude_list:
      continue
    cluster_name = "PC-A-PE-1" if i <= 100 else "PC-A-PE-2"
    print vm_name, cluster_name, ctr_name 
    v = vm_obj.get(vm_name=vm_name, cluster_name=cluster_name)
    vm_spec = v.spec
    vm_spec.pop("status")
     
    ctr_ref["storage_config"]["storage_container_reference"]["uuid"] = ctr_uuid 
    vm_spec["spec"]["resources"]["disk_list"][0] = cdrom_ref
    vm_spec["spec"]["resources"]["disk_list"][1] = image_ref
    vm_spec["spec"]["resources"]["disk_list"][2] = ctr_ref
    #print vm_spec
    print "Updating VM: {0}".format(vm_name)
    task = v.update(vm_spec) 
    task_map[vm_name] = task
    time.sleep(0.2)
  
print task_map 

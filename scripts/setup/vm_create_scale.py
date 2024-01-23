import time
from pprint import pprint
import sys
from framework.lib import *
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.cluster_entity import Cluster
from framework.ctr_entity import Ctr
from framework.vm_entity import VM
from framework.vg_entity import VG
from framework.subnet_entity import Subnet
from setup_config import *

IP = SRC_PC_IP
CLUS_LIST = SRC_CLUS_LIST
#IP = TGT_PC_IP
#CLUS_LIST = TGT_CLUS_LIST
clus_obj = Cluster(IP)
ctr_obj = Ctr(IP)
vm_obj = VM(IP)
vg_obj = VG(IP)
subnet_obj = Subnet(IP)

#image_map = {"name": "CentOS_7_2", "uuid": "3417f9e9-9997-4bfa-b187-18fdd116020e"}
#image_map = {"name": "RHEL_84", "uuid": "4dd57843-cf2f-4548-be3a-c8aaefa6d7c0"}
#image_map = {"name": "CentOS8-uefi", "uuid": "7986f02d-03c1-476a-a3dd-5d70030c9702"}
image_map = {"name": "CentOS8-uefi", "uuid": "7fe4a9f3-9508-46c4-a964-1abe5c6ab561"}
vm_name_uuid_map = vm_obj.get_name_uuid_map()
#vg_name_uuid_map = vg_obj.get_name_uuid_map()

for clus_name in CLUS_LIST:
  ctr_name_uuid_map = ctr_obj.get_name_uuid_map(cluster_name=clus_name)
  sub = subnet_obj.get(vlan_name="vlan0", cluster_name=clus_name)
  #subnet_map = {"name": "vlan0", "uuid": "651533ff-8df2-4c63-a34a-82f37e0aa93c"}
  subnet_map = {"name": "vlan0", "uuid": sub.uuid}
  clus = clus_obj.get(cluster_name=clus_name)
  clus_map = {"name": clus_name, "uuid": clus.uuid} 
  #clus_map = {"name": "PC-B-PE-1", "uuid": "0005f80c-8736-f085-0000-00000000ba23"} 

  if clus_name in ["PC-A-PE-1", "PC-B-PE-1"]:
    start, end = 1, 1001
  elif clus_name in ["PC-A-PE-2", "PC-B-PE-2"]:
    start, end = 101, 201
  for i in range(start, end):
    vm_name = "vm-scale-" + str(i)
    if vm_name in vm_name_uuid_map:
      print "{0} - {1} already present on cluster: {2}".format(vm_name, vm_name_uuid_map[vm_name], clus_name)
      continue
    print "Need to create VM: {0} on cluster: {1}".format(vm_name, clus_name)
    self_service_ctr_uuid = ctr_name_uuid_map["SelfServiceContainer"]
    #self_service_ctr_uuid = "4a17181d-efae-4716-a99e-d045060cc5c2" 
    vm_spec = get_vm_spec(vm_name, clus_map, image_map, subnet_map, self_service_ctr_uuid)
    vm_spec["spec"]["resources"]["boot_config"] = {"boot_type": "UEFI"}
    vm_spec["spec"]["resources"]["vtpm_config"] = {"vtpm_enabled": False} 
    #vm_spec["spec"]["resources"]["vtpm_config"] = {"vtpm_enabled": True} 
    #vm_spec["metadata"]["use_categories_mapping"] = True
    #vm_spec["metadata"]["categories_mapping"]= {"scale-cat": ["scale-val"]}
    #print(vm_spec)
    task_uuid = vm_obj.create(vm_spec)
    print "VM: {0}, Cluster: {1}, Create Task UUID: {2}".format(vm_name, clus_name, task_uuid)
    time.sleep(1)


"""
vg_spec = generate_vg_spec()
#pprint(vg_spec)
PC_IP = "10.40.216.116"
vg_obj = VG(PC_IP)
for vg_name in vg_spec:
  print "Creating VG: {0}".format(vg_name)
  spec = vg_spec[vg_name]["spec"]
  disk_list = vg_spec[vg_name]["disk_list"]
  task_url = vg_obj.create(vg_spec=spec)
  vg_spec[vg_name]["task_url"] = task_url
  time.sleep(2)
  vg = vg_obj.get(vg_name=vg_name)
  vg_uuid = vg.uuid
  print "Adding disks to the {0} - {1}".format(vg_name, vg_uuid)
  for disk_spec in disk_list:
    vg.add_disk(disk_spec=disk_spec)
"""

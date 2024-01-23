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
image_map = {"name": "CENTOS_79", "uuid": "c7edfdc6-f770-4752-b3f8-8066a1eadec8"}
vm_name_uuid_map = vm_obj.get_name_uuid_map()
#vg_name_uuid_map = vg_obj.get_name_uuid_map()

for clus_name in CLUS_LIST:
  ctr_name_uuid_map = ctr_obj.get_name_uuid_map(cluster_name=clus_name)
  sub = subnet_obj.get(vlan_name="vlan0", cluster_name=clus_name)
  subnet_map = {"name": "vlan0", "uuid": sub.uuid}
  clus = clus_obj.get(cluster_name=clus_name)
  #clus_map = {"name": clus_name, "uuid": clus.uuid} 
  clus_map = {"name": "PC-A-PE-1", "uuid": "0006026b-4d8f-dfb2-064c-ac1f6b1c671c"} 

  if clus_name in ["PC-A-PE-1", "PC-B-PE-1"]:
    start, end = 51, 55
  elif clus_name in ["PC-A-PE-2", "PC-B-PE-2"]:
    start, end = 101, 201
  for i in range(start, end):
    vm_name = "vm-" + str(i)
    if vm_name in vm_name_uuid_map:
      print "{0} - {1} already present on cluster: {2}".format(vm_name, vm_name_uuid_map[vm_name], clus_name)
      continue
    print "Need to create VM: {0} on cluster: {1}".format(vm_name, clus_name)
    self_service_ctr_uuid = ctr_name_uuid_map["SelfServiceContainer"]
    #self_service_ctr_uuid = "c0eb49f0-f36b-4590-801d-8941fcdb72bc"
    vm_spec = get_vm_spec(vm_name, clus_map, image_map, subnet_map, self_service_ctr_uuid)
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

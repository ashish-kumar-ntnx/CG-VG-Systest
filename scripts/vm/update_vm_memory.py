from framework.vm_entity import VM
from framework.image_entity import Image
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
from framework.mh_vm_entity import VM
#SETUP_TYPE == "ESX"
#if SETUP_TYPE == "ESX":
#elif SETUP_TYPE == "AHV":
#  from framework.vm_entity import VM

IP = TGT_PC_IP
#IP = SRC_PC_IP
vm_prefix = "vm-"
#vm_prefix = "Nutanix-Test-vm-"
IP = "10.46.144.59"

START = 1
END = 101
vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
print vm_name_uuid_map

def get_vm_host_uuid(v):
  vm_json = v.get_v1_json()
  vm_hyp_id = vm_json["hostUuid"]
  return vm_hyp_id

def vm_memory_update(vm_name, memory=1024):
  print "Updating memory of VM: {0} to {1} MB".format(vm_name, memory)
  vm_uuid = vm_name_uuid_map[vm_name]
  v = vm_obj.get(vm_uuid=vm_uuid)
  vm_hyp_id = get_vm_host_uuid(v)
  generic_dto = dict()
  generic_dto["uuid"] = vm_uuid
  generic_dto["name"] = vm_name
  generic_dto["description"] = "VM is {0}".format(vm_name)
  generic_dto["memory_mb"] = 1024
  generic_dto["num_vcpus"] = 1
  generic_dto["num_cores_per_vcpu"] = 1
  generic_dto["host_uuid"] = vm_hyp_id
  generic_dto["vm_features"] = {}
  spec_for_vm_update = [{"generic_dto": generic_dto, "cluster_uuid": "0005c79d-d6b9-66eb-0000-000000011f37"}]
  v.fanout_update(vm_spec=spec_for_vm_update)
"""
for i in range(1, 101):
  vm_name = "vm-{0}".format(i)
  if vm_name in vm_name_uuid_map:
    v = vm_obj.get(vm_uuid=vm_name_uuid_map[vm_name])
    #vm_hyp_id = get_vm_host_uuid(v)
    network_uuid = "1f0bb84f-fff6-4c7a-a5db-9e558998d3ac"
    adapter_type = "E1000"
    new_name = "vm-{0}".format(i)
    print "Adding NIC {0} to {1}".format(adapter_type, vm_name)
    v.fanout_add_nic(network_uuid, adapter_type)


for i in range(1, 101):
  vm_name = vm_prefix + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  v = vm_obj.get(vm_uuid=vm_uuid)
  print "Powering off VM: {0}".format(vm_name)
  power_state = "off"
  #print "Powering on VM: {0}".format(vm_name)
  #power_state = "on"
  v.fanout_power_state(power_state)

for i in range(1, 101):
  vm_name = vm_prefix + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  v = vm_obj.get(vm_uuid=vm_uuid)
  print "Powering on VM: {0}".format(vm_name)
  power_state = "on"
  v.fanout_power_state(power_state)


for i in range(1, 101, 10):
  for k in range(3):
    vm_name = vm_prefix + str(i + k)
    #print vm_name
    vm_memory_update(vm_name, memory=3072)
  for k in range(3, 10):
    vm_name = vm_prefix + str(i + k)
    #print vm_name
    vm_memory_update(vm_name, memory=1024)

  
#for i in range(START, END):
#  vm_uuid = vm_name_uuid_map[vm_name]
#  v = vm_obj.get(vm_uuid=vm_uuid) 
#  vm_memory_update(v, memory=1024)
"""
for i in range(1, 161):
  old_vm_name = "Nutanix-Test-ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(i).rjust(4, '0')
  new_vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(i).rjust(4, '0')
  if old_vm_name in vm_name_uuid_map:
    v = vm_obj.get(vm_uuid=vm_name_uuid_map[old_vm_name])
    vm_hyp_id = get_vm_host_uuid(v)
    print "Renaming {0} to {1}".format(old_vm_name, new_vm_name)
    v.fanout_vm_rename(new_vm_name, vm_hyp_id)



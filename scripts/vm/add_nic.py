import time
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

def nic_exists(v):
  vm_json = v.get_v1_json()
  vm_nics = vm_json["virtualNicIds"]
  if vm_nics == []:
    return False
  return True

def get_nic_mac(v):
  vm_json = v.get_v1_json()
  vm_nic = vm_json["virtualNicIds"][0]
  return vm_nic[-17:]

def vm_nic_remove(vm_name):
  vm_uuid = vm_name_uuid_map[vm_name]
  v = vm_obj.get(vm_uuid=vm_uuid)
  if nic_exists(v):
    mac = get_nic_mac(v)
    print "Removing NIC: {0} from VM: {1}".format(mac, vm_name)
    v.fanout_remove_nic(mac)
  

def vm_nic_add(vm_name, network_uuid, adapter_type):
  vm_uuid = vm_name_uuid_map[vm_name]
  v = vm_obj.get(vm_uuid=vm_uuid)
  if not nic_exists(v):
    print "Adding NIC: {0} from network: {1} to VM: {2}".format(adapter_type, network_uuid, vm_name)
    v.fanout_add_nic(network_uuid, adapter_type)

"""
for i in range(1, 101):
  vm_name = vm_prefix + str(i)
  vm_nic_remove(vm_name)
"""
#time.sleep(60)
for i in range(1, 101):
  vm_name = vm_prefix + str(i)
  vm_nic_add(vm_name, "https://10.45.73.26:9440/api/nutanix/v0.8/vms/nics/fanout", "E1000")

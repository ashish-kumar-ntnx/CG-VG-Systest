import sys
from pprint import pprint
from framework.vg_entity import VG
#from framework.vm_entity import VM
from framework.category_entity import Category
from framework.recovery_plan_entity import RecoveryPlan
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM

#IP = TGT_PC_IP
#IP = SRC_PC_IP
IP = "10.40.216.106"

vg_obj = VG(IP)
vm_obj = VM(IP)
cat_obj = Category(IP)
rp_obj = RecoveryPlan(IP)

DEFAULT_TARGET_SECRET = "Nutanix.1234"

#SOURCE_AZ = {"name": "PC-A", "UUID": "eb51b6f4-d8f2-4c58-8962-2b84bacceb88"}
#TARGET_AZ = {"name": "PC-B", "UUID": "d44e542d-6e29-435b-8e8d-229c6d58cd52"}
#SOURCE_CLUSTER_LIST = []
#TARGET_CLUSTER_LIST = []
#SOURCE_AZ_RECOVERY_NETWORK_LIST = ["vlan0"]
#TARGET_AZ_RECOVERY_NETWORK_LIST = ["vlan0"]
#SOURCE_AZ_TEST_NETWORK_LIST = ["vlan0"]
#TARGET_AZ_TEST_NETWORK_LIST = ["vlan0"]

SOURCE_AZ = {"name": "PC-A", "UUID": "5dd3b83c-0ed2-4186-8269-15474a3aa76b"}
TARGET_AZ = {"name": "PC-A", "UUID": "5dd3b83c-0ed2-4186-8269-15474a3aa76b"}
SOURCE_CLUSTER_LIST = [{"name": "PC-A-PE-1", "uuid": "0005c703-6b0c-9922-0000-0000000129b9"}]
TARGET_CLUSTER_LIST = [{"name": "PC-A-PE-2", "uuid": "0005c713-3e20-f4de-7111-0cc47a9b0c24"}]
SOURCE_AZ_RECOVERY_NETWORK_LIST = ["vlan0"]
TARGET_AZ_RECOVERY_NETWORK_LIST = ["VM Network"]
SOURCE_AZ_TEST_NETWORK_LIST = ["vlan0"]
TARGET_AZ_TEST_NETWORK_LIST = ["VM Network"]

def create_vg_list(vg_name_list, vg_name_uuid_map):
  volume_group_recovery_info_list = list()

  for vg_name in vg_name_list:
    tmp = dict()
    volume_group_config_info_list = list()
    vg_uuid = vg_name_uuid_map[vg_name]
    vg = vg_obj.get(vg_uuid=vg_uuid)
    t = dict()
    t["volume_group_reference"] = dict()
    t["volume_group_reference"]["kind"] = "volume_group"
    t["volume_group_reference"]["name"] = vg_name
    t["volume_group_reference"]["uuid"] = vg_uuid
    if vg.is_chap_enabled :
      t["authentication_type"] = "CHAP"
      t["target_secret"] = DEFAULT_TARGET_SECRET
    volume_group_config_info_list.append(t)
    tmp["volume_group_config_info_list"] = volume_group_config_info_list

    volume_reference = dict()
    volume_reference["kind"] = "volume_group"
    volume_reference["name"] = vg_name
    volume_reference["uuid"] = vg_uuid
    tmp["volume_group_reference"] = volume_reference      

    volume_group_recovery_info_list.append(tmp)
  return volume_group_recovery_info_list

def create_stage_list(vm_name_list, vm_name_uuid_map, vg_name_uuid_map, stage_delay=0, vg_list=None):
  stage_map = dict()
  stage_map["delay_time_secs"] = stage_delay
  stage_map["stage_work"] = dict()
  stage_map["stage_work"]["recover_entities"] = dict()
  entity_info_list = list()
  for vm_name in vm_name_list:
    tmp = dict()
    vm_uuid = vm_name_uuid_map[vm_name]
    any_entity_reference=dict()
    any_entity_reference["kind"] = "vm"
    any_entity_reference["name"] = vm_name
    any_entity_reference["uuid"] = vm_uuid
    tmp["any_entity_reference"] = any_entity_reference
    
    tmp["volume_group_attachment_list"] = list()

    tmp1 =dict()
    tmp1["vm_reference"] = dict()
    tmp1["vm_reference"]["kind"] = "vm" 
    tmp1["vm_reference"]["name"] = vm_name
    tmp1["vm_reference"]["uuid"] = vm_uuid

    tmp1["volume_group_attachment_info_list"] = list()

    if not vg_list:
      vg_list = get_vgs_attached_to_vm(vm_name) 
    volume_group_attachment_info_list = list()
    for vg_name in vg_list:
      vg_uuid = vg_name_uuid_map[vg_name]
      k = dict()
      k["attachment_type"] = "IQN"
      k["volume_group_reference"] = dict()
      k["volume_group_reference"]["kind"] = "volume_group"
      k["volume_group_reference"]["name"] = vg_name
      k["volume_group_reference"]["uuid"] = vg_uuid
      volume_group_attachment_info_list.append(k)

    tmp1["volume_group_attachment_info_list"] = volume_group_attachment_info_list 
    tmp["volume_group_attachment_list"].append(tmp1)
    entity_info_list.append(tmp)
      
  stage_map["stage_work"]["recover_entities"]["entity_info_list"] = entity_info_list
  return stage_map

def get_vgs_attached_to_vm(vm_name):
  vg_list = list()
  vm_index = int(vm_name.split("-")[1])
  if vm_index < 101:
    vg_list.append("vg-a-" + str(vm_index))
    vg_list.append("vg-a-" + str(vm_index + 100))
  else:
    vg_list.append("vg-b-" + str(vm_index - 100))
    vg_list.append("vg-b-" + str(vm_index))
  return vg_list

def create_rp_parameters(source_az_map, target_az_map):
  parameters = dict()
  parameters["primary_location_index"] = 0
  parameters["floating_ip_assignment_list"] = list()
  parameters["availability_zone_list"] = list()
  parameters["network_mapping_list"] = list()
  parameters["network_mapping_list"] = list()
  availability_zone_network_mapping_list = list()
  for i in [source_az_map, target_az_map]:
    tmp = dict()
    tmp["cluster_reference_list"] = i["cluster_reference_list"]
    tmp["availability_zone_url"] = i["uuid"]
    parameters["availability_zone_list"].append(tmp)
    tmp = dict()
    tmp["cluster_reference_list"] = i["cluster_reference_list"]
    tmp["availability_zone_url"] = i["uuid"]
    tmp["recovery_network"] = {"name": i["recovery_network"]}
    tmp["test_network"] = {"name": i["test_network"]}
    availability_zone_network_mapping_list.append(tmp)
  parameters["network_mapping_list"].append({"availability_zone_network_mapping_list": availability_zone_network_mapping_list})
  return parameters 
  
def get_final_rp_spec(rp_name, volume_group_recovery_info_list, stage_list, rp_params):
  rp_spec = dict()
  rp_spec["spec"] = dict()
  rp_spec["metadata"] = dict()
  rp_spec["metadata"]["kind"] = "recovery_plan"
  rp_spec["api_version"] = "3.1"
  rp_spec["spec"]["name"] = rp_name
  rp_spec["spec"]["description"] = rp_name + " for cg_vg system test"
  rp_spec["spec"]["resources"] = dict()
  rp_spec["spec"]["resources"]["volume_group_recovery_info_list"] = volume_group_recovery_info_list
  rp_spec["spec"]["resources"]["stage_list"] = stage_list
  rp_spec["spec"]["resources"]["parameters"] = rp_params
  
  return rp_spec  

if __name__=="__main__":
  #source_az_map = {"uuid": "089f4290-b5d1-40f5-a0b5-fcc3aef5c36b", "recovery_network": "vlan0", "test_network": "vlan0", "cluster_reference_list": [{"kind": "cluster", "name": "PC-A-PE-1", "uuid": "0005c6fe-1e48-3c4e-3045-ac1f6b15d8c2"}]}
  #target_az_map = {"uuid": "089f4290-b5d1-40f5-a0b5-fcc3aef5c36b", "recovery_network": "vlan0", "test_network": "vlan0", "cluster_reference_list": [{"kind": "cluster", "name": "PC-A-PE-2", "uuid": "0005c703-6b0c-9922-0000-0000000129b9"}]}
  source_az_map = {"uuid": "d55a7f4e-47bd-45cc-8370-796fb592ddc9", "recovery_network": "vlan0", "test_network": "vlan0", "cluster_reference_list": []}
  target_az_map = {"uuid": "c391fad3-0a42-4176-9fa2-0c1f467e6fdd", "recovery_network": "vlan0", "test_network": "vlan0", "cluster_reference_list": []}
  #source_az_map = {"uuid": "5bf36d0e-60fa-4fe1-b7c4-386ca4a69527", "recovery_network": "VM Network", "test_network": "VM Network", "cluster_reference_list": []}
  #target_az_map = {"uuid": "31d8a95b-62e8-4305-b7f9-86f5da0817f8", "recovery_network": "VM Network", "test_network": "VM Network", "cluster_reference_list": []}

  rp_params = create_rp_parameters(source_az_map, target_az_map)
  vm_name_uuid_map = vm_obj.get_name_uuid_map()
  vm_uuid_name_map = vm_obj.get_uuid_name_map()
  vg_uuid_name_map = vg_obj.get_uuid_name_map()
  vg_name_uuid_map = vg_obj.get_name_uuid_map()


  vm_name_list = ["ak-vm-1", "ak-vm-2"]
  vg_name_list = ["ak-vg-1", "ak-vg-2"]
  rp_name = "ak-rp"
  print "Creating Recovery Plan: {0}".format(rp_name)
  stage_map = create_stage_list(vm_name_list, vm_name_uuid_map, vg_name_uuid_map, stage_delay=0, vg_list=vg_name_list)
  stage_list = [stage_map]
  volume_group_recovery_info_list = create_vg_list(vg_name_list, vg_name_uuid_map)
  rp_spec = get_final_rp_spec(rp_name, volume_group_recovery_info_list, stage_list, rp_params)
  rp_obj.create(spec=rp_spec)
  #print rp_spec
  print "########\n"

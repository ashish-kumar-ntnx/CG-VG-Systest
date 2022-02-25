import sys
from pprint import pprint
from framework.vg_entity import VG
from framework.vm_entity import VM
from framework.category_entity import Category
from framework.recovery_plan_entity import RecoveryPlan
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
#IP = SRC_PC_IP

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

def create_vg_list(vg_type, categories_list, vg_uuid_name_map):
  volume_group_recovery_info_list = list()
  for i in categories_list:
    tmp = dict()
    cat_key, cat_val = i.keys()[0], i.values()[0]
    c = cat_obj.get(cat_key=cat_key, cat_val=cat_val)
    vm_list, vg_list = c.get_entities()
    volume_group_config_info_list = list()
    for vg_uuid in vg_list:
      vg = vg_obj.get(vg_uuid=vg_uuid)
      vg_name = vg_uuid_name_map[vg_uuid]
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
    if vg_type == "category":
      tmp["category_filter"] = dict()
      tmp["category_filter"]["type"] = "CATEGORIES_MATCH_ANY"
      tmp["category_filter"]["params"] = dict()
      tmp["category_filter"]["params"][cat_key] = [cat_val]
    volume_group_recovery_info_list.append(tmp)
  return volume_group_recovery_info_list

def create_stage_list(vm_type, categories_list, vm_uuid_name_map, vg_name_uuid_map, stage_delay=0):
  stage_map = dict()
  stage_map["delay_time_secs"] = stage_delay
  stage_map["stage_work"] = dict()
  stage_map["stage_work"]["recover_entities"] = dict()
  entity_info_list = list()
  for i in categories_list:
    tmp = dict()
    cat_key, cat_val = i.keys()[0], i.values()[0]
    if vm_type == "category":
      tmp["categories"] = {cat_key: cat_val}

    volume_group_attachment_list = list()
    c = cat_obj.get(cat_key=cat_key, cat_val=cat_val)
    vm_list, vg_list = c.get_entities()
    for vm_uuid in vm_list:
      vm_name = vm_uuid_name_map[vm_uuid]
      t = dict()
      t["vm_reference"] = dict()
      t["vm_reference"]["kind"] = "vm" 
      t["vm_reference"]["name"] = vm_name
      t["vm_reference"]["uuid"] = vm_uuid
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
      t["volume_group_attachment_info_list"] = volume_group_attachment_info_list 
      volume_group_attachment_list.append(t)
    tmp["volume_group_attachment_list"] = volume_group_attachment_list
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
  #source_az_map = {"uuid": "5dd3b83c-0ed2-4186-8269-15474a3aa76b", "recovery_network": "vlan0", "test_network": "vlan0", "cluster_reference_list": [{"kind": "cluster", "name": "PC-A-PE-1", "uuid": "0005c703-6b0c-9922-0000-0000000129b9"}]}
  #target_az_map = {"uuid": "5dd3b83c-0ed2-4186-8269-15474a3aa76b", "recovery_network": "VM Network", "test_network": "VM Network", "cluster_reference_list": [{"kind": "cluster", "name": "PC-A-PE-2", "uuid": "0005c713-3e20-f4de-7111-0cc47a9b0c24"}]}
  source_az_map = {"uuid": "e4ba3e3a-d6bc-4aaf-8a5e-d71f7119eddf", "recovery_network": "vlan0", "test_network": "vlan0", "cluster_reference_list": []}
  target_az_map = {"uuid": "089f4290-b5d1-40f5-a0b5-fcc3aef5c36b", "recovery_network": "vlan0", "test_network": "vlan0", "cluster_reference_list": []}
  vg_type = "category"
  vm_type = "category"
  rp_params = create_rp_parameters(source_az_map, target_az_map)
  vm_uuid_name_map = vm_obj.get_uuid_name_map()
  vg_uuid_name_map = vg_obj.get_uuid_name_map()
  vg_name_uuid_map = vg_obj.get_name_uuid_map()
  cat_list = list()
  for i in range(1, 11, 5):
    tmp = list()
    for j in range(5):
      tmp.append({"cat-" + str(i+j) : "val-" + str(i+j)})
    cat_list.append(tmp)
  for i in range(2):
    rp_name = "new-rp-50-vms-" + str(i + 1)
    categories_list = cat_list[i]
    print "\n########"
    print "Creating Recovery Plan: {0}".format(rp_name)
    volume_group_recovery_info_list = create_vg_list(vg_type, categories_list, vg_uuid_name_map)
    stage_map = create_stage_list(vm_type, categories_list, vm_uuid_name_map, vg_name_uuid_map, stage_delay=0)
    stage_list = [stage_map]
    rp_spec = get_final_rp_spec(rp_name, volume_group_recovery_info_list, stage_list, rp_params)
    rp_obj.create(spec=rp_spec)
    print "########\n"
  #print vm_uuid_name_map
  #sys.exit()
  #print volume_group_recovery_info_list
  #pprint(rp_params)
  #print stage_map
  #print rp_spec

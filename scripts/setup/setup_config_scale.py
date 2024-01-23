from base_specs import vm_spec
import random

vm_prefix = "vm-"
num_vms = 200
vg_a_prefix = "vg-scale-"
num_vgs_a = 200
vg_b_prefix = "vg-b-"
num_vgs_a = 200
vg_disk_count = 10
vg_disk_size_list = [1, 3]
ctr_prefix = "cg-vg-ctr-"
num_ctrs = 20
cat_key_prefix = "cat-"
cat_val_prefix = "val-"
num_cats = 20
clus_list = ["PC-A-PE-1", "PC-A-PE-2"]


def get_vg_list(vg_prefix, start, end):
  vg_list = list()
  for i in range(start, end):
    vg_list.append(vg_prefix + str(i))
  return vg_list

def get_vm_list(start, end):
  vm_list = list()
  for i in range(start, end):
    vm_list.append(vm_prefix + str(i))
  return vm_list

def get_ctr_list(start, end):
  ctr_list = list()
  for i in range(start, end + 1):
    ctr_list.append(ctr_prefix + str(i))
  return ctr_list

def get_config_map(clus):
  if clus in ["PC-A-PE-1", "PC-B-PE-1"]:
    ctr_start = 1
    ctr_end = 10
    vg_prefix = vg_a_prefix
    vg_start = 1
    vg_end = 2001
    vm_start = 1
    vm_end = 100
  elif clus in ["PC-A-PE-2", "PC-B-PE-2"]:
    ctr_start = 1
    ctr_end = 10
    vg_prefix = vg_b_prefix
    vg_start = 1
    vg_end = 200
    vm_start = 101
    vm_end = 200

  config_map = dict()
  ctr_list = get_ctr_list(ctr_start, ctr_end)
  vg_list = get_vg_list(vg_prefix, vg_start, vg_end)
  vm_list = get_vm_list(vm_start, vm_end)
  config_map = dict()
  config_map["ctr_list"] = ctr_list
  config_map["vg_list"] = vg_list
  config_map["vm_list"] = vm_list
  return config_map
 
def get_vm_spec(vm_name, clus_map, image_map, subnet_map, self_service_ctr_uuid) :
  #vm_spec = dict()
  vm_spec["spec"]["name"] = vm_name
  clus_map["kind"] = "cluster"
  image_map["kind"] = "image"
  subnet_map["kind"] = "subnet"
  vm_spec["spec"]["cluster_reference"] = clus_map
  vm_spec["spec"]["resources"]["disk_list"][1]["data_source_reference"] = image_map
  vm_spec["spec"]["resources"]["nic_list"][0]["subnet_reference"] = subnet_map
  vm_spec["spec"]["resources"]["disk_list"][2]["storage_config"]["storage_container_reference"]["uuid"] = self_service_ctr_uuid
  return vm_spec

def get_vg_spec(vg_name, cluster_name, cluster_uuid, ctr_name_uuid_map, disk_count=1, disk_size_range=[1], vg_password="Nutanix.1234", create_vg_with_chap=False):
  config_map = get_config_map(cluster_name)
  ctr_list = config_map["ctr_list"]
  #vg_list = config_map["vg_list"]
  ctr_uuid_list = [ctr_name_uuid_map[i] for i in ctr_list]
  #print ctr_uuid_list
  vg_spec = dict()
  tmp = dict()
  tmp["name"] = vg_name
  tmp["description"] = "VG : {0}".format(vg_name)
  tmp["sharingStatus"] = "SHARED"
  tmp["iscsiTargetPrefix"] = vg_name
  if create_vg_with_chap:
    tmp["targetSecret"] = vg_password
    tmp["enabledAuthentications"] = "CHAP"
  tmp["clusterReference"] = cluster_uuid
  vg_spec["spec"] = tmp
  vg_spec["disk_list"] = list()
  for i in range(disk_count):
    tmp = dict()
    ctr_uuid = random.choice(ctr_uuid_list)
    disk_size = random.choice(disk_size_range)
    tmp["diskSizeBytes"] = disk_size * 1024 * 1024 * 1024
    tmp["diskDataSourceReference"] = {"extId": ctr_uuid, "entityType": "STORAGE_CONTAINER"}
    vg_spec["disk_list"].append(tmp) 
  return vg_spec 

if __name__=="__main__":
  for i in clus_list:
    config_map = get_config_map(i)
    print config_map


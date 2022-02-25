from tinydb import TinyDB, Query
from lib import *

vm_spec = {"metadata":{"categories_mapping":{},"kind":"vm","use_categories_mapping":True},"spec":{"name":"template-centos_72_2","cluster_reference":{"uuid":"0005c337-953d-05ae-0000-0000000109fe","name":"PC-A-PE-1","kind":"cluster"},"resources":{"gpu_list":[],"memory_size_mib":2048,"boot_config":{"boot_type":"LEGACY","boot_device":{"disk_address":{"device_index":0,"adapter_type":"SCSI"}}},"disk_list":[{"device_properties":{"device_type":"CDROM","disk_address":{"adapter_type":"SATA","device_index":0}}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":0}},"data_source_reference":{"kind":"image","uuid":"75946783-05a1-4c37-b7f1-dc09d3653d13","name":"centos_72"}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":1}},"disk_size_bytes":5368709120,"storage_config":{"storage_container_reference":{"kind":"storage_container","uuid":"f7286a99-fd92-4153-8e17-4e3bc4fbed13"}}}],"num_vcpus_per_socket":1,"num_sockets":1,"hardware_clock_timezone":"UTC","nic_list":[{"is_connected":True,"subnet_reference":{"uuid":"c2b83ab6-e689-4bf5-bf7c-ebcb196c8e8d","kind":"subnet"}}]}},"api_version":"3.1.0"}

image_db = TinyDB("../db/image.json")
ctr_db = TinyDB("../db/ctr.json")
cluster_db = TinyDB("../db/cluster.json")
category_db = TinyDB("../db/category.json")
subnet_db = TinyDB("../db/subnet.json")
vm_small_db = TinyDB("../db/vm_small_spec.json")
vm_ext_db = TinyDB("../db/vm_extended_spec.json")

vm_dict = dict()
vm_table = vm_small_db.table()
for i in vm_table.all():
  vm_name = i["name"]
  spec = i["spec"]
  ids = GetIds(spec)
  vm_spec["spec"]["name"] = vm_name

  vm_spec["spec"]["cluster_reference"]["uuid"] = ids.cluster_id
  vm_spec["spec"]["cluster_reference"]["name"] = spec["cluster"]

  vm_spec["spec"]["resources"]["nic_list"][0]["subnet_reference"]["uuid"] = ids.subnet_id

  vm_spec["spec"]["resources"]["disk_list"][1]["data_source_reference"]["uuid"] = ids.image_id
  vm_spec["spec"]["resources"]["disk_list"][1]["data_source_reference"]["name"] = spec["image"]

  vm_spec["spec"]["resources"]["disk_list"][2]["disk_size_bytes"] = spec["disk_size_bytes"]
  vm_spec["spec"]["resources"]["disk_list"][2]["storage_config"]["storage_container_reference"]["uuid"] = ids.ctr_id

  vm_spec["metadata"]["categories_mapping"] = {spec["cat_key"]: [spec["cat_val"]]}

  vm_dict[vm_name] = vm_spec
  vm_ext_db.insert({"name": vm_name, "spec": vm_spec})
  
  
  

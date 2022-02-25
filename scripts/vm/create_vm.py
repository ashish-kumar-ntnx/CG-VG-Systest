from framework.lib import *
from framework.vm_entity import VM
from framework.cluster_entity import Cluster
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

vm_obj = VM(SRC_PC_IP)
clus_obj = Cluster(SRC_PC_IP)

vm_spec = {"metadata":{"categories_mapping":{},"kind":"vm","use_categories_mapping":True},"spec":{"name":"template-centos_72_2","cluster_reference":{"uuid":"0005c337-953d-05ae-0000-0000000109fe","name":"PC-A-PE-1","kind":"cluster"},"resources":{"gpu_list":[],"memory_size_mib":2048,"boot_config":{"boot_type":"LEGACY","boot_device":{"disk_address":{"device_index":0,"adapter_type":"SCSI"}}},"disk_list":[{"device_properties":{"device_type":"CDROM","disk_address":{"adapter_type":"SATA","device_index":0}}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":0}},"data_source_reference":{"kind":"image","uuid":"75946783-05a1-4c37-b7f1-dc09d3653d13","name":"centos_72"}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":1}},"disk_size_bytes":5368709120,"storage_config":{"storage_container_reference":{"kind":"storage_container","uuid":"f7286a99-fd92-4153-8e17-4e3bc4fbed13"}}}],"num_vcpus_per_socket":1,"num_sockets":1,"hardware_clock_timezone":"UTC","nic_list":[{"is_connected":True,"subnet_reference":{"uuid":"c2b83ab6-e689-4bf5-bf7c-ebcb196c8e8d","kind":"subnet"}}]}},"api_version":"3.1.0"}

pe_1_uuid = ""
pe_2_uuid = ""
cluster_uuid_list = list()
for clus in ["PC-A-PE-1", "PC-A-PE-2"]:
  c = clus_obj.get(cluster_name=clus)
  cluster_uuid_list.append(c.uuuid)

vm_spec_map = dict()

for i in range(1, 101):
  for ctr 

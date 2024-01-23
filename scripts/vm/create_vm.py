from framework.lib import *
from framework.vm_entity import VM
from framework.cluster_entity import Cluster
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

SRC_PC_IP = "10.40.188.162"
#vm_obj = VM(SRC_PC_IP)
#clus_obj = Cluster(SRC_PC_IP)

#vm_spec = {"metadata":{"categories_mapping":{},"kind":"vm","use_categories_mapping":True},"spec":{"name":"template-centos_72_2","cluster_reference":{"uuid":"0005c337-953d-05ae-0000-0000000109fe","name":"PC-A-PE-1","kind":"cluster"},"resources":{"gpu_list":[],"memory_size_mib":2048,"boot_config":{"boot_type":"LEGACY","boot_device":{"disk_address":{"device_index":0,"adapter_type":"SCSI"}}},"disk_list":[{"device_properties":{"device_type":"CDROM","disk_address":{"adapter_type":"SATA","device_index":0}}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":0}},"data_source_reference":{"kind":"image","uuid":"75946783-05a1-4c37-b7f1-dc09d3653d13","name":"centos_72"}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":1}},"disk_size_bytes":5368709120,"storage_config":{"storage_container_reference":{"kind":"storage_container","uuid":"f7286a99-fd92-4153-8e17-4e3bc4fbed13"}}}],"num_vcpus_per_socket":1,"num_sockets":1,"hardware_clock_timezone":"UTC","nic_list":[{"is_connected":True,"subnet_reference":{"uuid":"c2b83ab6-e689-4bf5-bf7c-ebcb196c8e8d","kind":"subnet"}}]}},"api_version":"3.1.0"}

vm_spec = {"metadata":{"categories_mapping":{},"kind":"vm","use_categories_mapping":True},"spec":{"name":"vm-1","resources":{"is_agent_vm":False,"vtpm_config":{"vtpm_enabled":True},"memory_overcommit_enabled":False,"num_sockets":1,"memory_size_mib":2048,"num_vcpus_per_socket":1,"hardware_clock_timezone":"UTC","disk_list":[{"device_properties":{"device_type":"CDROM","disk_address":{"adapter_type":"SATA","device_index":0}},"storage_config":{"storage_container_reference":{"kind":"storage_container","uuid":"efb8de19-658b-4259-b3a5-8669dded63d1","name":"default-container-88253"}}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":0}},"disk_size_bytes":107374182400,"storage_config":{"storage_container_reference":{"kind":"storage_container","uuid":"efb8de19-658b-4259-b3a5-8669dded63d1","name":"default-container-88253"}},"data_source_reference":{"kind":"image","uuid":"92f20a3f-5ee5-4680-bc2d-3b3d159da084","name":"win11_22h2_ent_sb"}},{"device_properties":{"device_type":"DISK","disk_address":{"adapter_type":"SCSI","device_index":1}},"disk_size_bytes":5368709120,"storage_config":{"storage_container_reference":{"kind":"storage_container","uuid":"5fc1448f-4631-4abe-8f62-0fa3de36f7e9","name":"SelfServiceContainer"}}}],"gpu_list":[],"boot_config":{"boot_type":"UEFI"},"nic_list":[]},"cluster_reference":{"uuid":"0005ed69-ca69-8191-0000-0000000158bd","kind":"cluster"}},"api_version":"3.1.0"}

for i in range(2, 101):
  vm_spec["spec"]["name"] = "vm-" + str(i)
  print("Creating: {0}".format("vm-" + str(i)))
  send_request("POST", SRC_PC_IP, "/api/nutanix/v3/vms", json=vm_spec)

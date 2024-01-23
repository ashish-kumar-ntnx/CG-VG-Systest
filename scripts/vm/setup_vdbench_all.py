import sys
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time
import threading

IP = TGT_PC_IP
CLUS_LIST = TGT_CLUS_LIST
IP = SRC_PC_IP
CLUS_LIST = SRC_CLUS_LIST
VM_PREFIX = "vm-"

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
START, END = 1, 161

def vdbench_enable(vm_name):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  v1.execute("mkdir -p /home/nutanix")
  print "Enabling vdbench on VM: {0} - {1}".format(vm_name, vm_uuid)
  v1.enable_vdbench()

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0')
    x = threading.Thread(target=vdbench_enable, args=(vm_name,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

#from framework.vm_entity import VM
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time
import threading

IP = SRC_PC_IP
#IP = TGT_PC_IP
vm_obj = VM(IP)
vm_obj = VM(IP)

vm_name_uuid_map = vm_obj.get_name_uuid_map()

GATEWAY = "10.45.128.1"
PREFIX = 17
START=1
END=101

def set_static(vm_name):
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  vm_ip = v1.get_vm_ip()
  cmd = 'nmcli con mod "System eth0" ipv4.addresses {0}/{1} ipv4.gateway {2} ipv4.method manual'.format(vm_ip, PREFIX, GATEWAY)
  _, out = v1.execute(cmd)
  print out

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0')
    x = threading.Thread(target=set_static, args=(vm_name,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

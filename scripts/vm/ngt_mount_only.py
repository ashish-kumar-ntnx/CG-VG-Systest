#from framework.vm_entity import VM
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
from framework.cluster_entity import Cluster
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time
import threading

IP = SRC_PC_IP
PE_NAME = SRC_CLUS_LIST[0]
#IP = TGT_PC_IP
#PE_NAME = TGT_CLUS_LIST[0]
vm_obj = VM(IP)

clus_obj = Cluster(IP)
clus = clus_obj.get(cluster_name=PE_NAME)
pe_v1_ip = clus.get_v1_ip()

vm_name_uuid_map = vm_obj.get_name_uuid_map()


def ngt_cmd(vm_name, pe_v1_ip):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  v1.mount_ngt(pe_v1_ip)

START=1
END=101
for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = "vm-" + str(j)
    x = threading.Thread(target=ngt_cmd, args=(vm_name, pe_v1_ip, ))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

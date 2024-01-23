from framework.vm_entity import VM
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import threading
import time

START = 1
END = 161
vm_obj = VM(SRC_PC_IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
#vm_exclude_list = ["vm-" + str(i) for i in range(151, 166)]

def enable_iscsi_and_generate_new_iqn(vm_name):
  print "\n#### VM: {0} ####".format(vm_name)
  vm_uuid = vm_name_uuid_map[vm_name]
  v = vm_obj.get(vm_uuid=vm_uuid)
  #v = vm_obj.get(vm_name=vm_name, cluster_name=cluster_name)
  v.enable_iscsi()
  print "Old IQN: {0}".format(v.get_iqn())
  v.generate_new_iqn()
  print "New IQN: {0}".format(v.iqn)
  

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0')
    x = threading.Thread(target=enable_iscsi_and_generate_new_iqn, args=(vm_name, ))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

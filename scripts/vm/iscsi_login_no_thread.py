#from framework.vm_entity import VM
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
from framework.cluster_entity import Cluster
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, DEFAULT_CHAP_PASSWORD, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time

#IP = TGT_PC_IP
#CLUS_LIST = TGT_CLUS_LIST
IP = SRC_PC_IP
CLUS_LIST = SRC_CLUS_LIST

vm_obj = VM(IP)


vm_name_uuid_map = vm_obj.get_name_uuid_map()

cluster_obj = Cluster(IP)
c1 = cluster_obj.get(cluster_name=CLUS_LIST[0])
c1_dsip = c1.get_dsip()
#c1_dsip = "10.45.135.0"
#c2 = cluster_obj.get(cluster_name=CLUS_LIST[1])
#c2_dsip = c2.get_dsip()
c2_dsip = None

sd_disk_map = dict()

vm_list = list()
for i in range(1, 101, 10):
  for j in range(3):
    vm_list.append("vm-" + str(i+j))

DISK_LENGTH = 21
START = 51
END = 101
for i in range(START, END):
  if i < 101:
    dsip = c1_dsip
  else:
    dsip = c2_dsip

  vm_name = "vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  len_disks = len(v1.get_sd_disk_list().split(" "))
  if len_disks == DISK_LENGTH:
    continue
  print "\n#### VM: {0}, {1} doing iscsi target_login ####".format(vm_name, vm_uuid)
  cmd = "sudo systemctl restart iscsid"
  v1.execute(cmd)
  if vm_name not in vm_list:
    v1.iscsi_target_login(dsip=dsip)
  else:
    v1.iscsi_target_login(dsip=dsip, target_chap_secret=DEFAULT_CHAP_PASSWORD)
  time.sleep(0.2)
  print "{0}, {1} Disks".format(vm_name, len(v1.get_sd_disk_list().split(" ")))
  #break

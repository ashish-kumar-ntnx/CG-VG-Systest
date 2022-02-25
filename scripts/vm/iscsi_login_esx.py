from framework.mh_vm_entity import VM
from framework.cluster_entity import Cluster
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time

SRC_PC_IP = "10.40.216.116"
vm_obj = VM(SRC_PC_IP)
TARGET_CHAP = "Nutanix.1234"


#vm_name_uuid_map = vm_obj.get_name_uuid_map()

cluster_obj = Cluster(SRC_PC_IP)
c1 = cluster_obj.get(cluster_name="SOURCE-PE")
dsip = c1.get_dsip()

sd_disk_map = dict()

for i in range(1, 2):
  vm_name = "ak-vm-1-210628-113054"
  #vm_name = "ak-vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  print "\n#### VM: {0}, {1} doing iscsi target_login ####".format(vm_name, vm_uuid)
  v1 = vm_obj.get(vm_uuid)
  v1.iscsi_target_login(dsip=dsip, target_chap_secret=TARGET_CHAP)
  #v1.iscsi_target_logout(dsip=dsip)
  time.sleep(0.2)
  #sd_disk_map[vm_name] = v1.get_sd_disk_list()
  print "{0}, {1} Disks".format(vm_name, len(v1.get_sd_disk_list().split(" ")))
  #break

#for vm in sd_disk_map:
#  print "{0}, {1} Disks".format(len(sd_disk_map[vm]))
#print sd_disk_map

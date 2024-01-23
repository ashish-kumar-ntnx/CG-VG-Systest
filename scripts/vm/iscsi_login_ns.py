#from framework.vm_entity import VM
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
from framework.cluster_entity import Cluster
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, DEFAULT_CHAP_PASSWORD, SETUP_TYPE
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

vm_obj = VM(IP)


vm_name_uuid_map = vm_obj.get_name_uuid_map()

#cluster_obj = Cluster(IP)
#c1 = cluster_obj.get(cluster_name=CLUS_LIST[0])
#c1_dsip = c1.get_dsip()
c1_dsip = "10.53.128.98"
#c1_dsip = "10.45.129.42" #"10.45.135.4"
c1_dsip = "10.45.140.189" #"10.45.135.4"
#c1_dsip = "10.45.129.42" #"10.45.135.4"
#c1_dsip = "10.45.141.222" #"10.45.140.203"
#c1_dsip = "10.45.140.203" #"10.45.140.203"
#c1_dsip = "10.45.129.44"
c1_dsip = "10.45.133.142"
#c1_dsip = "10.45.133.24"
c1_dsip = "10.45.140.221"
#c1_dsip = "10.45.135.4"
#c2 = cluster_obj.get(cluster_name=CLUS_LIST[1])
#c2_dsip = c2.get_dsip()
c2_dsip = None

sd_disk_map = dict()

DISK_LENGTH = 2
#DISK_LENGTH = 4
START, END = 1, 161

vm_list = list()
for i in range(START, END, 10):
  for j in range(3):
    vm_list.append("vm-" + str(i+j))
vm_name_list = []
vm_list = [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100]
vm_name_list = ["ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0') for j in vm_list]

def _login(vm_name, dsip):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  cmd = "rpm -e nutanix-guest-agent-255.0-1.x86_64"
  _, out = v1.execute(cmd)
  print out
  

def login(vm_name, dsip):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  sd_disk_list = v1.get_sd_disk_list()
  if sd_disk_list == "\n":
    len_disks = 0
  else:
    len_disks = len(sd_disk_list.split(" "))
  if len_disks == DISK_LENGTH:
    return
  #cmd = "rm -rf /var/lib/iscsi/nodes/*"
  #_, out = v1.execute(cmd)
  print "\n#### VM: {0}, {1} doing iscsi target_login ####".format(vm_name, vm_uuid)
  #cmd = "systemctl restart iscsid"
  #v1.execute(cmd)
  time.sleep(0.2)
  v1.iscsi_target_login(dsip=dsip)
  #if vm_name not in vm_name_list:
  #  v1.iscsi_target_login(dsip=dsip)
  #else:
  #  v1.iscsi_target_login(dsip=dsip, target_chap_secret=DEFAULT_CHAP_PASSWORD)
  #print "{0}, {1} Disks".format(vm_name, len(v1.get_sd_disk_list().split(" ")))
  

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    dsip = c1_dsip
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0')
    #x = threading.Thread(target=login, args=(vm_name, dsip,))
    x = threading.Thread(target=login, args=(vm_name, dsip,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()
    

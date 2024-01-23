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
#c1_dsip = "10.45.135.4" #"10.45.141.222"
#c1_dsip = "10.45.141.222"
c1_dsip = "10.53.128.98"
#c1_dsip = "10.45.129.42"
c1_dsip = "10.45.140.221"
#c1_dsip = "10.45.140.189"
#c1_dsip = "10.45.129.38"
#c1_dsip = "10.45.141.222" #"10.45.140.203"
#c1_dsip = "10.45.140.203"
#c1_dsip = "10.45.141.238"
#c1_dsip = "10.45.141.238"
#c1_dsip = "10.45.133.24"
#c1_dsip = "10.45.129.41"
#c2 = cluster_obj.get(cluster_name=CLUS_LIST[1])
#c2_dsip = c2.get_dsip()
c2_dsip = None

START = 1
END = 161

#START, END = 11, 21

def logout(vm_name, dsip):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  print "\n#### VM: {0}, {1} doing iscsi target_logout ####".format(vm_name, vm_uuid)
  v1.iscsi_target_logout(dsip=dsip)
  time.sleep(0.2)

  cmd = "rm -rf /var/lib/iscsi/nodes/*"
  _, out = v1.execute(cmd)
  print out

  print "{0}, {1} Disks".format(vm_name, len(v1.get_sd_disk_list().split(" ")))
  

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    dsip = c1_dsip
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0')
    x = threading.Thread(target=logout, args=(vm_name, dsip,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()
    

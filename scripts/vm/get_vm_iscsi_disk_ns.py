from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
from framework.cluster_entity import Cluster
import time
import threading

IP = SRC_PC_IP
CLUS_LIST = SRC_CLUS_LIST
#IP = TGT_PC_IP
#CLUS_LIST = TGT_CLUS_LIST
VM_PREFIX = "vm-"
#VM_PREFIX = "Nutanix-Test-vm-"

#IP = SRC_PC_IP
#CLUS_LIST = SRC_CLUS_LIST
#VM_PREFIX = "Nutanix-Test-vm-"

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()

#DISK_LENGTH = 21
DISK_LENGTH = 2
START = 1
END = 161

vm_with_less_disk_count = dict()
vm_with_auth_failure = list()

def check_disk_count(vm_name):
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  try:
    v1 = vm_obj.get(vm_uuid)
    out = v1.execute("iscsiadm -m session")
    print out
    sd_disk_list = v1.get_sd_disk_list()
    if sd_disk_list == "\n":
      len_disks = 0
    else: 
      len_disks = len(sd_disk_list.split(" "))
    print "IQN: {0}".format(v1.get_iqn())
    print "{0}, {1} Disks\n".format(vm_name, len_disks)
    if len_disks != DISK_LENGTH:
      print "IQN: {0}".format(v1.get_iqn())
      print "{0}, {1} Disks\n".format(vm_name, len_disks)
      print "ALERT!!!! VM: {0}".format(vm_name)
      vm_with_less_disk_count[vm_name] = len_disks
  except:
    vm_with_auth_failure.append(vm_name)

for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    #vm_name = VM_PREFIX + str(j)
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0') 
    x = threading.Thread(target=check_disk_count, args=(vm_name,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

if vm_with_less_disk_count:
  print "List of vms which have less disks"
  for vm_name, disk_count in vm_with_less_disk_count.iteritems():
    print "VM: {0}, DISK_COUNT: {1}".format(vm_name, disk_count)

if vm_with_auth_failure:
  print "vms with auth failure: {0}".format(vm_with_auth_failure)

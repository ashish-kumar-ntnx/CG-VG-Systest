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

vm_name_uuid_map = vm_obj.get_name_uuid_map()


"""
vm_list = list()
for i in range(1, 101, 10):
  for j in range(3):
    vm_list.append("vm-" + str(i+j))
vm_list = ['vm-12', 'vm-15', 'vm-18', 'vm-19', 'vm-21', 'vm-23', 'vm-25', 'vm-27', 'vm-31', 'vm-32', 'vm-33', 'vm-34', 'vm-37', 'vm-38', 'vm-4', 'vm-45', 'vm-52', 'vm-9']
"""
vm_list = ['ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0043', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0044', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0046', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0048', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0049', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0052', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0054', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0056', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0058', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0060', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0062', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0063', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0064', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0065', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0066', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0071', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0073', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0074', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0075', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0077', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0079', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0122', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0126', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0128', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0130', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0132', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0134', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0135', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0141', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0143', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0145', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0146', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0149', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0151', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0152', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0155', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0160']

def ngt_cmd(vm_name):
  #if vm_name not in vm_list:
  #  return
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  print "triggering ngt install on vm: {0}".format(vm_name)
  cmd = "mkdir -p /tmp/mnt; mount /dev/sr0 /tmp/mnt; sleep 1; /tmp/mnt/installer/linux/install_ngt.py"
  #cmd = "/usr/local/nutanix/ngt/python36/python3 /tmp/mnt/installer/linux/install_ngt.py"
  #cmd = "mkdir -p /tmp/mnt; sudo mount /dev/sr0 /tmp/mnt; sudo /tmp/mnt/installer/linux/install_ngt.py"
  #cmd = "sudo mount /dev/sr0 /tmp/mnt; sudo /tmp/mnt/installer/linux/install_ngt.py"
  #cmd = "sudo hostnamectl set-hostname {0}".format(vm_name)
  _, out = v1.execute(cmd)
  print out

START=1
END=161
for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(j).rjust(4, '0')
    #vm_name = "vm-" + str(j)
    x = threading.Thread(target=ngt_cmd, args=(vm_name, ))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

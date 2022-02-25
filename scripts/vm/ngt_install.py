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

"""
vm_list = list()
for i in range(1, 101, 10):
  for j in range(3):
    vm_list.append("vm-" + str(i+j))
vm_list = ['vm-12', 'vm-15', 'vm-18', 'vm-19', 'vm-21', 'vm-23', 'vm-25', 'vm-27', 'vm-31', 'vm-32', 'vm-33', 'vm-34', 'vm-37', 'vm-38', 'vm-4', 'vm-45', 'vm-52', 'vm-9']
"""

def ngt_cmd(vm_name):
  print "triggering ngt install on vm: {0}".format(vm_name)
  if vm_name not in vm_name_uuid_map:
    return
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  cmd = "mkdir /tmp/mnt; sudo mount /dev/sr0 /tmp/mnt; sudo /tmp/mnt/installer/linux/install_ngt.py"
  #cmd = "sudo mount /dev/sr0 /tmp/mnt; sudo /tmp/mnt/installer/linux/install_ngt.py"
  #cmd = "sudo hostnamectl set-hostname {0}".format(vm_name)
  _, out = v1.execute(cmd)
  print out

START=1
END=101
for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vm_name = "vm-" + str(j)
    x = threading.Thread(target=ngt_cmd, args=(vm_name,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

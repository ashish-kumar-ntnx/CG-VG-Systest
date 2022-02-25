from framework.mh_vm_entity import VM
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time
SRC_PC_IP = "10.40.216.116"
vm_obj = VM(SRC_PC_IP)

vm_name_uuid_map = vm_obj.get_name_uuid_map()


START=1
END=10
for i in range(START, END):
  vm_name = "ak-vm-" + str(i)
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  #v1.execute("sudo hostnamectl set-hostname {0}".format(vm_name))
  #v1.execute("sudo yum install zip unzip java -y")
  v1.enable_vdbench()

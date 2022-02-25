#from framework.vm_entity import VM
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time

IP = SRC_PC_IP
#IP = TGT_PC_IP
vm_obj = VM(IP)
vm_obj = VM(IP)

vm_name_uuid_map = vm_obj.get_name_uuid_map()

vm_list = list()
for i in range(1, 101, 10):
  for j in range(3):
    vm_list.append("vm-" + str(i+j))
vm_list = ['vm-12', 'vm-15', 'vm-18', 'vm-19', 'vm-21', 'vm-23', 'vm-25', 'vm-27', 'vm-31', 'vm-32', 'vm-33', 'vm-34', 'vm-37', 'vm-38', 'vm-4', 'vm-45', 'vm-52', 'vm-9']

START=1
END=101
for i in range(START, END):
  vm_name = "vm-" + str(i)
  #if vm_name not in vm_list:
  #  continue
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  #cmd = 'echo "nutanix ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'
  #cmd = 'echo -e "nutanix/4u\n" | sudo -S sh -c "echo \'nutanix ALL=(ALL) NOPASSWD:ALL\' >> /etc/sudoers"'
  #cmd = 'echo "nutanix ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'
  cmd = "sudo hostnamectl set-hostname {0}".format(vm_name)
  _, out = v1.execute(cmd)
  #cmd = "sudo bash; mkdir /tmp/mnt; mount /dev/sr0 /tmp/mnt; cd /tmp/mnt/installer/linux/; ./install_ngt.py"
  #cmd = "mkdir /tmp/mnt; sudo mount /dev/sr0 /tmp/mnt; sudo /tmp/mnt/installer/linux/install_ngt.py"
  #cmd = "sudo hostnamectl set-hostname {0}; sudo yum makecache fast; sudo yum install iscsi-initiator-utils -y; /usr/sbin/iscsid -version".format(vm_name)
  #cmd = "sudo yum clean all; sudo yum makecache fast; sudo yum install iscsi-initiator-utils -y; /usr/sbin/iscsid -version".format(vm_name)
  #cmd = "cd /etc/yum.repos.d/; sudo rm iso.repo iso2.repo; sudo wget http://filer.dev.eng.nutanix.com:8080/Users/ashish.kumar/centos-8-repo/centos-8-repo.zip; sudo unzip centos-8-repo.zip; cd /etc/pki/rpm-gpg/; sudo wget http://filer.dev.eng.nutanix.com:8080/Users/ashish.kumar/centos-8-repo/centos-8-pkg-key.zip; sudo unzip centos-8-pkg-key.zip; sudo yum install -y java"
  #cmd = "/usr/sbin/iscsid -version"
  #cmd = "sudo rm -rf /home/nutanix/vdbench50407/vdbench_output/*".format(vm_name)
  #cmd = "sudo hostnamectl set-hostname {0}; sudo yum makecache fast; sudo yum clean all".format(vm_name)
  #cmd = "sudo yum makecache fast; sudo yum clean all"
  #cmd = "sudo rm -rf /var/log/*"
  _, out = v1.execute(cmd)
  print out
  #v1.enable_iscsi()

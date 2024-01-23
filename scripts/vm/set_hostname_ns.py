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

vm_name_uuid_map = vm_obj.get_name_uuid_map()

vm_list = list()
for i in range(1, 101, 10):
  for j in range(3):
    vm_list.append("vm-" + str(i+j))
#vm_list = ['vm-89', 'vm-98', 'vm-99', 'vm-96', 'vm-97', 'vm-94', 'vm-100']
vm_list = [147, 158, 150, 153, 155, 114, 110]

vm_list = ['ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0027', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0118', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0034', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0040', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0033', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0019', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0100', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0088', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0098', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0105', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0014', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0106', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0081', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0036', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0084', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0104', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0113', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0092', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0037', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0022', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0031', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0032', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0029', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0099', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0028', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0091', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0082', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0085', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0018']
vm_list = ['ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0004', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0010', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0015', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0018', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0024', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0064', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0069', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0081', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0082', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0085', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0086', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0088', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0089', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0102', 'ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_0106']
START=1
END=161
#END=101
failed_vm_list = list()
for i in range(START, END):
  #if i not in vm_list:
  #  continue
  #vm_name = "DB-VM-" + str(i)
  vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(i).rjust(4, '0')
  #vm_name = "vm-" + str(i)
  if vm_name not in vm_list:
    continue
  if vm_name not in vm_name_uuid_map:
    print vm_name
  vm_uuid = vm_name_uuid_map[vm_name]
  v1 = vm_obj.get(vm_uuid)
  #cmd = "sudo yum install java -y"
  #_, out = v1.execute(cmd)
  #cmd = "sudo sed -i 's/=enforcing/=disabled/' /etc/selinux/config"
  #_, out = v1.execute(cmd)
  #cmd = "yum install wget -y; wget http://uranus.corp.nutanix.com/~ashish.kumar/fdisk_format.sh; sh fdisk_format.sh"
  #_, out = v1.execute(cmd)
  #print out
  #cmd = 'echo "nutanix ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'
  #cmd = 'echo -e "nutanix/4u\n" | sudo -S sh -c "echo \'nutanix ALL=(ALL) NOPASSWD:ALL\' >> /etc/sudoers"'
  #cmd = 'echo "nutanix ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers'
  #cmd = "sudo hostnamectl set-hostname {0}".format(vm_name)
  cmd = "hostnamectl set-hostname {0}".format(vm_name)
  #cmd = "hostnamectl set-hostname {0}; yum makecache fast; yum install iscsi-initiator-utils -y; /usr/sbin/iscsid -version".format(vm_name)
  #_, out = v1.execute(cmd)
  #cmd = "fdisk -l"
  #cmd = "chmod +x /home/nutanix/setup_vdbench50407.sh; /home/nutanix/setup_vdbench50407.sh"
  #cmd = "cat /etc/rc.d/rc.local |grep vdbench"
  #cmd = "cat /home/nutanix/vdbench50407/my_vdbench_param.txt | grep sd= |wc -l;ps -ef |grep vdbench"
  #cmd = "rm -rf /var/lib/iscsi/nodes/*"
  #cmd = "sed -i 's/VD_FILE=.*/VD_FILE=\/home\/nutanix\/vdbench50407\/my_vdbench_param.txt/g' /home/nutanix/vdbench50407/create_vd_bench_param.sh; cat /home/nutanix/vdbench50407/create_vd_bench_param.sh"
  #cmd = "cat /home/nutanix/vdbench50407/my_vdbench_param.txt"
  #cmd = "rm -f /home/nutanix/vdbench50407/my_vdbench_param.txt; wget http://uranus.corp.nutanix.com/~ashish.kumar/my_vdbench_param.txt -P /home/nutanix/vdbench50407"
  #cmd = "sed -i 's/sudo //g' /etc/rc.local"
  #cmd = "sed -i '\/root\/start_vdbench_vdi/d' /etc/rc.local"
  #cmd = "sed -i 's/sudo fdisk/\/usr\/sbin\/fdisk/g' /home/nutanix/vdbench50407/create_vd_bench_param.sh; /usr/bin/sh /home/nutanix/vdbench50407/create_vd_bench_param.sh; grep SD -A2 /home/nutanix/vdbench50407/my_vdbench_param.txt; grep vdbench /etc/rc.local"
  #cmd = "/usr/bin/sh /home/nutanix/vdbench50407/create_vd_bench_param.sh; grep SD -A4 /home/nutanix/vdbench50407/my_vdbench_param.txt; grep vdbench /etc/rc.local"
  #_, out = v1.execute(cmd)
  #print out
  #cmd = "sed -i 's/\/home\/nutanix\/vdbench50407\/vdbench\.sh//g' /etc/rc.local; cd /etc/systemd/system/; wget http://uranus.corp.nutanix.com/~ashish.kumar/vdbench-exec.service; systemctl enable vdbench-exec.service; systemctl start vdbench-exec.service"
  #cmd = "sed -i 's/sudo //' /home/nutanix/vdbench50407/create_vd_bench_param.sh"
  #_, out = v1.execute(cmd)
  #print out
  #cmd = "ps -ef |grep vdbench"
  #cmd = "rpm -e nutanix-guest-agent-255.0-1.x86_64"
  #cmd = "cd /home/nutanix/vdbench50407/; /usr/bin/sh create_vd_bench_param.sh ; cat /home/nutanix/vdbench50407/my_vdbench_param.txt | grep lun"
  #_, out = v1.execute(cmd)
  #print out
  #cmd = "sudo sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*; sudo sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*; sudo yum makecache --refresh"
  #_, out = v1.execute(cmd)
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
  #cmd = "sudo rm -rf /var/lib/iscsi/nodes/*"
  #_, out = v1.execute(cmd)
  #v1.enable_iscsi()/home/nutanix/vdbench50407/my_vdbench_param.txt
  #cmd = "rm -f /usr/local/nutanix/ngt/dotenv.json; systemctl restart ngt_guest_agent"
  #cmd = "hostnamectl set-hostname {0}; cd /home/nutanix/; wget http://uranus.corp.nutanix.com/~ashish.kumar/setup_vdbench50407_root_systest.sh; chmod +x /home/nutanix/setup_vdbench50407_root_systest.sh; /home/nutanix/setup_vdbench50407_root_systest.sh".format(vm_name)
  try:
    _, out = v1.execute(cmd)
  except:
    print "Failed for VM: {0}".format(vm_name)
    failed_vm_list.append(vm_name)
  print out
print failed_vm_list

from framework.cg_entity import CG
#from framework.vm_entity import VM
from framework.vg_entity import VG
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM

IP = TGT_PC_IP
IP = SRC_PC_IP
cg = CG(IP)
vm = VM(IP)
vg = VG(IP)


vm_name_uuid_map = vm.get_name_uuid_map()
vg_name_uuid_map = vg.get_name_uuid_map()
#vg_name_uuid_map = vg.get_name_uuid_map(cluster_uuid="0005c6fe-1e48-3c4e-3045-ac1f6b15d8c2")
#print len(vg_name_uuid_map)
#print " ".join(vg_name_uuid_map.keys())
#print vm_name_uuid_map
vm_num = 81
vg_num = 81
START, END = 9, 17

for i in range(START, END):
  cg_name = "cg-" + str(i)
  vm_name_list, vg_name_list = [], []
  vm_list, vg_list = [], []
  for j in range(10):
    vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + str(vm_num).rjust(4, '0')
    vm_name_list.append(vm_name)
    vm_list.append(vm_name_uuid_map[vm_name])

    vg_name = "vdi-vm-{0}-vg-1".format(vg_num)
    vg_name_list.append(vg_name)
    vg_list.append(vg_name_uuid_map[vg_name])
    vg_name = "vdi-vm-{0}-vg-2".format(vg_num)
    vg_name_list.append(vg_name)
    vg_list.append(vg_name_uuid_map[vg_name])
    vg_num += 1
    vm_num += 1

  print "Creating CG: {0}, with vms: {1}, vgs: {2}".format(cg_name, vm_name_list, vg_name_list)
  cg.create(cg_name, vm_list, vg_list)
  #print cg_name
  #print vm_name_list
  #print vg_name_list
  #print vm_list
  #print vg_list
  print "\n"

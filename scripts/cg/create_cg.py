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

vm_num = 1
vg_num_a = 1
vg_num_b = 1
#vm_num = 21
#vg_num_a = 21

vm_name_uuid_map = vm.get_name_uuid_map()
vg_name_uuid_map = vg.get_name_uuid_map()
#vg_name_uuid_map = vg.get_name_uuid_map(cluster_uuid="0005c6fe-1e48-3c4e-3045-ac1f6b15d8c2")
#print len(vg_name_uuid_map)
#print " ".join(vg_name_uuid_map.keys())
#print vm_name_uuid_map

for i in range(1, 11):
  cg_name = "cg-" + str(i)
  #pe_name = "PC-A-PE-1" if i < 11 else "PC-A-PE-2"
  vg_prefix= "vg-a-" if i < 11 else "vg-b-"

  vm_name_list, vg_name_list = [], []
  vm_list, vg_list = [], []
  for j in range(10):
    vm_name = "vm-" + str(vm_num)
    vm_name_list.append(vm_name)
    vm_list.append(vm_name_uuid_map[vm_name])
    vm_num += 1

    if vg_prefix == "vg-a-":
      vg_name = vg_prefix + str(vg_num_a)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_name = vg_prefix + str(vg_num_a + 100)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_num_a += 1
    else:
      vg_name = vg_prefix + str(vg_num_b)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_name = vg_prefix + str(vg_num_b + 100)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_num_b += 1

  print "Creating CG: {0}, with vms: {1}, vgs: {2}".format(cg_name, vm_name_list, vg_name_list)
  cg.create(cg_name, vm_list, vg_list)
  #print cg_name
  #print vm_name_list
  #print vg_name_list
  #print vm_list
  #print vg_list
  print "\n"

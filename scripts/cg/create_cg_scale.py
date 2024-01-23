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

vg_name_uuid_map = vg.get_name_uuid_map()
#vg_name_uuid_map = vg.get_name_uuid_map(cluster_uuid="0005c6fe-1e48-3c4e-3045-ac1f6b15d8c2")
#print len(vg_name_uuid_map)
#print " ".join(vg_name_uuid_map.keys())
#print vm_name_uuid_map

cg_name = "scale_cg"

vg_name_list = []
vg_prefix= "vg-scale-"
for i in range(1, 31):
  vg_name_list.append(vg_prefix + str(i))

vg_list = [vg_name_uuid_map[i] for i in vg_name_list]

print "Creating CG: {0}, with vms: {1}, vgs: {2}".format(cg_name, [], vg_name_list)
cg.create(cg_name, [], vg_list)

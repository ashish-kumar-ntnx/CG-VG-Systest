import time
from pprint import pprint
#from vg_spec_generator import generate_vg_spec
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST


vg = VG(SRC_PC_IP)
#vg = VG(TGT_PC_IP)

vg_name_uuid_map = vg.get_name_uuid_map()
#print vg_name_uuid_map

vg_prefix = "vg-a-"
#vg_prefix = "DB-VG-"
#vg_prefix_list = ["Nutanix-Test-vg-a-"]
#vg_prefix_list = ["vg-a-", "vg-b-"]

for i in range(1, 201):
  #vg_name = vg_prefix + str(i)
  vg_name = "vdi-vm-{0}-vg-1".format(i)
  if vg_name not in vg_name_uuid_map:
    continue
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj = vg.get(vg_uuid=vg_uuid)
  disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
  #remove_disk_list = disk_uuid_list[10:] 
  remove_disk_list = disk_uuid_list
  for disk_uuid in remove_disk_list:
    print "Removing disk {0} from VG: {1} - {2}".format(disk_uuid, vg_name, vg_uuid)
    vg_obj.remove_disk(disk_uuid)

"""
for i in range(1, 201):
  vg_name_list = [j + str(i) for j in vg_prefix_list]
  #vg_name_list = ["vg-a-" + str(i), "vg-b-" + str(i)]
  #if i < 101:
  #  vg_name = "vg-a-" + str(i)
  #else:
  #  vg_name = "vg-b-" + str(i)
  for vg_name in vg_name_list:
    vg_uuid = vg_name_uuid_map[vg_name]
    vg_obj = vg.get(vg_uuid=vg_uuid)
    disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
    remove_disk_list = disk_uuid_list[10:] 
    for disk_uuid in remove_disk_list:
      print "Removing disk {0} from VG: {1} - {2}".format(disk_uuid, vg_name, vg_uuid)
      vg_obj.remove_disk(disk_uuid)
"""

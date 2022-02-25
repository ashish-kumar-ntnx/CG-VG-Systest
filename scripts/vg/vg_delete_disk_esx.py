import time
from pprint import pprint
#from vg_spec_generator import generate_vg_spec
from framework.vg_entity import VG
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = "10.40.216.116"


vg = VG(IP)

vg_name_uuid_map = vg.get_name_uuid_map()
print vg_name_uuid_map
for i in range(1, 21):
  vg_name = "ak-vg-" + str(i)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj = vg.get(vg_uuid=vg_uuid)
  disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
  remove_disk_list = disk_uuid_list[10:] 
  for disk_uuid in remove_disk_list:
    print "Removing disk {0} from VG: {1} - {2}".format(disk_uuid, vg_name, vg_uuid)
    vg_obj.remove_disk(disk_uuid)

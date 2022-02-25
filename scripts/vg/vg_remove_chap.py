import sys
import time
from pprint import pprint
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = SRC_PC_IP
#IP = TGT_PC_IP
vg = VG(IP)

vg_name_uuid_map = vg.get_name_uuid_map()

#for i in range(1, 11):
for i in range(51, 101):
  #vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i), "vg-b-" + str(i), "vg-b-" + str(100 + i)]
  vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i)]
  for vg_name in vg_name_list:
    vg_uuid = vg_name_uuid_map[vg_name]
    print "Removing CHAP from VG: {0} - {1}".format(vg_name, vg_uuid)
    vg_obj=vg.get(vg_uuid=vg_uuid)
    vg_obj.remove_chap()

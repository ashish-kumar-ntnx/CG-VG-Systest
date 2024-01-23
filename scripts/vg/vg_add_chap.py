import sys
import time
from pprint import pprint
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, DEFAULT_CHAP_PASSWORD

IP = SRC_PC_IP
#IP = TGT_PC_IP
vg = VG(IP)

vg_name_uuid_map = vg.get_name_uuid_map()

for i in range(101, 155):
  vg_name = "vg-a-{0}".format(i)
  vg_uuid = vg_name_uuid_map[vg_name]
  print "Adding CHAP password: {0} from VG: {1} - {2}".format(DEFAULT_CHAP_PASSWORD, vg_name, vg_uuid)
  vg_obj=vg.get(vg_uuid=vg_uuid)
  vg_obj.add_chap(DEFAULT_CHAP_PASSWORD)
  
  
"""
for i in range(1, 201, 10):
  for j in range(3):
    vg_name = "vg-a-{0}".format(i + j)
    vg_uuid = vg_name_uuid_map[vg_name]
    print "Adding CHAP password: {0} from VG: {1} - {2}".format(DEFAULT_CHAP_PASSWORD, vg_name, vg_uuid)
    vg_obj=vg.get(vg_uuid=vg_uuid)
    vg_obj.add_chap(DEFAULT_CHAP_PASSWORD)

#for i in range(1, 11):
#for i in range(1, 101, 10):
for i in range(1, 101):
  #vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i), "vg-b-" + str(i), "vg-b-" + str(100 + i)]
  vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i)]
  for vg_name in vg_name_list:
    vg_uuid = vg_name_uuid_map[vg_name]
    print "Adding CHAP password: {0} from VG: {1} - {2}".format(DEFAULT_CHAP_PASSWORD, vg_name, vg_uuid)
    vg_obj=vg.get(vg_uuid=vg_uuid)
    vg_obj.add_chap(DEFAULT_CHAP_PASSWORD)
"""

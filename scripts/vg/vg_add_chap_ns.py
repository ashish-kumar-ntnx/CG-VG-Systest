import sys
import time
from pprint import pprint
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, DEFAULT_CHAP_PASSWORD

IP = SRC_PC_IP
#IP = TGT_PC_IP
vg = VG(IP)

vg_name_uuid_map = vg.get_name_uuid_map()

for i in range(21, 41):
  vg_name = "vdi-vm-{0}-vg-1".format(i)
  vg_uuid = vg_name_uuid_map[vg_name]
  print "Adding CHAP password: {0} from VG: {1} - {2}".format(DEFAULT_CHAP_PASSWORD, vg_name, vg_uuid)
  vg_obj=vg.get(vg_uuid=vg_uuid)
  vg_obj.add_chap(DEFAULT_CHAP_PASSWORD)

for i in range(81, 101):
  vg_name = "vdi-vm-{0}-vg-1".format(i)
  vg_uuid = vg_name_uuid_map[vg_name]
  print "Adding CHAP password: {0} from VG: {1} - {2}".format(DEFAULT_CHAP_PASSWORD, vg_name, vg_uuid)
  vg_obj=vg.get(vg_uuid=vg_uuid)
  vg_obj.add_chap(DEFAULT_CHAP_PASSWORD)
  vg_name = "vdi-vm-{0}-vg-2".format(i)
  vg_uuid = vg_name_uuid_map[vg_name]
  print "Adding CHAP password: {0} from VG: {1} - {2}".format(DEFAULT_CHAP_PASSWORD, vg_name, vg_uuid)
  vg_obj=vg.get(vg_uuid=vg_uuid)
  vg_obj.add_chap(DEFAULT_CHAP_PASSWORD)

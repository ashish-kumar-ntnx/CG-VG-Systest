import time
from pprint import pprint
#from vg_spec_generator import generate_vg_spec
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = SRC_PC_IP
#IP = TGT_PC_IP
vg = VG(IP)

vg_name_uuid_map = vg.get_name_uuid_map()
#print vg_name_uuid_map
#vg_prefix_a = "Nutanix-Test-vg-a-"
vg_prefix_a = "vg-a-"

vg_less_count_a = 0
vg_ok_count_a = 0
vg_less_count_b = 0
vg_ok_count_b = 0
for i in range(1, 201):
  vg_name = vg_prefix_a + str(i)
  if vg_name not in vg_name_uuid_map:
    continue
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj = vg.get(vg_uuid=vg_uuid)
  disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
  if len(disk_uuid_list) != 10:
    vg_less_count_a += 1
    print "**** For VG: {0} - {1}, disk_count: {2}".format(vg_name, vg_uuid, len(disk_uuid_list))
  else:
    vg_ok_count_a += 1
    print "For VG: {0} - {1}, disk_count: {2}".format(vg_name, vg_uuid, len(disk_uuid_list))
"""
for i in range(1, 201):
  vg_name = "vg-b-" + str(i)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj = vg.get(vg_uuid=vg_uuid)
  disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
  if len(disk_uuid_list) != 10:
    vg_less_count_b += 1
    print "**** For VG: {0} - {1}, disk_count: {2}".format(vg_name, vg_uuid, len(disk_uuid_list))
  else:
    vg_ok_count_b += 1
    print "For VG: {0} - {1}, disk_count: {2}".format(vg_name, vg_uuid, len(disk_uuid_list))
"""
print "vg_less_count_a: {0}".format(vg_less_count_a)
print "vg_ok_count_a: {0}".format(vg_ok_count_a)
print "vg_less_count_b: {0}".format(vg_less_count_b)
print "vg_ok_count_b: {0}".format(vg_ok_count_b)

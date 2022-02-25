from framework.vg_entity import VG
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#IP = TGT_PC_IP
IP = SRC_PC_IP
#SRC_PC_IP = "10.40.216.116"
v = VG(IP)
c = Category(IP)
#vg_list = v.list_all()["data"]
#vg_objects = list()
  
#vg_objets = [v.get(vg_uuid = i["extId"]) for i in vg_list]

vg_name_uuid_map = v.get_name_uuid_map()

START = 1
END = 10
VG_PREFIX = "Nutanix-Test-vg-a-"

for i in range(START, END + 1):
  vg_name = "Nutanix-Test-vg-a-" + str(i)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg = v.get(vg_uuid=vg_uuid)
  print "#####"
  print "VG-NAME: {0}, VG-UUID: {1}".format(vg.name, vg.uuid)
  cat_list = vg.get_categories()
  if not cat_list:
    print "No Category is attached to this VG"
  for i in cat_list:
    cat_uuid = i["extId"]
    _c = c.get(cat_uuid=cat_uuid) 
    print "CAT_KEY: {0}, CAT_VAL: {1}, CAT_UUID: {2}".format(_c.cat_key, _c.cat_val, cat_uuid)
  print "#####\n"
  


"""

for i in vg_list:
  vg = v.get(vg_uuid = i["extId"])
  print "#####"
  print "VG-NAME: {0}, VG-UUID: {1}".format(vg.name, vg.uuid)
  cat_list = vg.get_categories()
  for i in cat_list:
    cat_uuid = i["extId"]
    _c = c.get(cat_uuid=cat_uuid) 
    print "CAT_KEY: {0}, CAT_VAL: {1}, CAT_UUID: {2}".format(_c.cat_key, _c.cat_val, cat_uuid)
  print "#####\n"
"""

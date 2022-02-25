import sys
from framework.vg_entity import VG
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#IP = TGT_PC_IP
IP = "10.40.216.116"
v = VG(IP)
c = Category(IP)

vg_name = sys.argv[1]

vg = v.get(vg_name=vg_name)
print "\n########"
print "VG-NAME: {0}, VG-UUID: {1}".format(vg.name, vg.uuid)
cat_list = vg.get_categories()
if not cat_list:
  print "No Category is attached to this VG"
for i in cat_list:
  cat_uuid = i["extId"]
  _c = c.get(cat_uuid=cat_uuid) 
  print "CAT_KEY: {0}, CAT_VAL: {1}, CAT_UUID: {2}".format(_c.cat_key, _c.cat_val, cat_uuid)
print "########\n"

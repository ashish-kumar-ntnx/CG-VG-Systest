import sys
from framework.vg_entity import VG
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#IP = TGT_PC_IP
IP = SRC_PC_IP

vg_obj = VG(IP)
vg_name_uuid_map = vg_obj.get_name_uuid_map()
cat_obj = Category(IP)

if len(sys.argv) != 6:
  print "\n\tUsage: python add_category_to_single_vg.py <vg_prefix> <vg_start> <vg_end> <cat_key> <cat_val>\n"
  sys.exit(1)
vg_pre = sys.argv[1]
vg_start = int(sys.argv[2])
vg_end = int(sys.argv[3])

cat_key = sys.argv[4]
cat_val = sys.argv[5]

cat = cat_obj.get(cat_key=cat_key, cat_val=cat_val)

for i in range(vg_start, vg_end):
  vg_name = vg_pre + str(i)
  vg = vg_obj.get(vg_name=vg_name)
  print "VG: {0} - {1} adding category: ({2}, {3})".format(vg_name, vg.uuid, cat_key, cat_val)
  vg.add_category(cat_uuid=cat.uuid)

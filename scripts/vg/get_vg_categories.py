from framework.vg_entity import VG
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
IP = SRC_PC_IP

vg_obj = VG(IP)
cat_obj = Category(IP)
vg_name_uuid_map = vg_obj.get_name_uuid_map()
#cat_key_uuid_map = cat_obj.get_key_uuid_map()
#cat_uuid_key_map = dict(zip(cat_key_uuid_map.values(), cat_key_uuid_map.keys()))

START, END = 1, 101
vg_pre = "vg-a-"
#vg_pre = "vg-b-"
#vg_pre = "Nutanix-Test-vg-a-"
#vg_pre = "Nutanix-Test-vg-b-"
no_category_vg_map = dict()

for i in range(START, END):
  for vg_name in [vg_pre + str(i), vg_pre + str(i + 100)]:
    if vg_name not in vg_name_uuid_map:
      continue
    vg_uuid = vg_name_uuid_map[vg_name]
    v = vg_obj.get(vg_uuid=vg_uuid)
    if len(v.category_list) != 0:
      cat_uuid_list = [i["extId"] for i in v.category_list]
      for vg_cat_uuid in cat_uuid_list:
        cat = cat_obj.get(cat_uuid=vg_cat_uuid)
        print "VG: {0} - {1}, Category: ({2}: {3}) - {4}".format(vg_name, vg_uuid, cat.cat_key, cat.cat_val, vg_cat_uuid)
    else:
      print "VG: {0} - {1}, No category found".format(vg_name, vg_uuid)
      no_category_vg_map[vg_name] = vg_uuid
print no_category_vg_map

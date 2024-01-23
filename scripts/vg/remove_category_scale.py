from framework.vg_entity import VG
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
IP = SRC_PC_IP

vg_obj = VG(IP)
cat_obj = Category(IP)
vg_name_uuid_map = vg_obj.get_name_uuid_map()
cat_key_uuid_map = cat_obj.get_key_uuid_map()

vgs = []
#vgs_1 = ["vg-a-" + str(i) for i in range(1, 101)]
#vgs_2 = ["vg-a-" + str(i) for i in range(101, 201)]
vgs = ["vg-scale-" + str(i) for i in range(1,31)]
#vgs_2 = ["vg-a-" + str(i) for i in range(101, 111)]
#vgs = vgs_1 + vgs_2
#vgs = vgs_1
#print vgs
for vg_name in vgs:
  if vg_name not in vg_name_uuid_map:
    continue
  vg_uuid = vg_name_uuid_map[vg_name]
  vg = vg_obj.get(vg_uuid=vg_uuid)
  vg_categories = [i["extId"] for i in vg.category_list] 
  for cat_uuid in vg_categories:
    #cat = cat_obj.get(cat_uuid=cat_uuid)
    #print "Removing category: {0}, ({1} : {2}) from VG: {3} -{4}".format(cat_uuid, cat.cat_key, cat.cat_val, vg_name, vg_uuid)
    print "Removing category: {0} from VG: {1} -{2}".format(cat_uuid, vg_name, vg_uuid)
    vg.remove_category(cat_uuid=cat_uuid)


from framework.vg_entity import VG
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, PROTECTION_TYPE

IP = TGT_PC_IP
IP = SRC_PC_IP

vg_obj = VG(IP)
cat_obj = Category(IP)
vg_name_uuid_map = vg_obj.get_name_uuid_map()
cat_key_uuid_map = cat_obj.get_key_uuid_map()

vgs = []
vgs_1 = ["vdi-vm-{0}-vg-1".format(i) for i in range(1, 81)]
vgs_2 = ["vdi-vm-{0}-vg-1".format(i) for i in range(81, 161)]
vgs_3 = ["vdi-vm-{0}-vg-2".format(i) for i in range(81, 161)]
#vgs_2 = ["vg-a-" + str(i) for i in range(101, 201)]
#vgs_1 = ["vg-b-" + str(i) for i in range(111, 131)]
#vgs_1 = ["vg-b-" + str(i) for i in range(111, 131)]
#vgs_1 = ["vg-b-" + str(i) for i in range(32, 111)]
#vgs_2 = ["vg-b-" + str(i) for i in range(11, 31)]
#vgs_2 = ["vg-b-" + str(i) for i in range(1, 11)]
#vgs_3 = ["vg-b-" + str(i) for i in range(132, 201)]
vgs = vgs_1 + vgs_2 + vgs_3
#print vgs
#vgs = ["vg-a-1", "vg-a-2"]

def get_vg_category_list():
  vg_category_list = list()
  vg_index = 1
  #for i in range(1, 17):
  for i in range(1, 17):
    if PROTECTION_TYPE == "category":
      #cat_key = "self-az-cat-" + str(i)
      cat_key = "cat-" + str(i)
      cat_val = "val-" + str(i)
    elif PROTECTION_TYPE == "explicit":
      cat_key = "ProtectionRule"
      cat_val = "pr-" + str(i)
    #cat_uuid = cat_key_uuid_map[cat_key]
    cat = cat_obj.get(cat_key=cat_key, cat_val=cat_val)
    #print cat.uuid
    cat_uuid = cat.uuid
    for _ in range(10):
      if i > 8:
        vg_name_list = ["vdi-vm-{0}-vg-1".format(vg_index), "vdi-vm-{0}-vg-2".format(vg_index)]
      else:
        vg_name_list = ["vdi-vm-{0}-vg-1".format(vg_index)]
      vg_index += 1
      for vg_name in vg_name_list:
        if vg_name not in vgs:
          continue
        if vg_name not in vg_name_uuid_map:
          continue
        vg_uuid = vg_name_uuid_map[vg_name]
        vg_category_list.append({"vg_name": vg_name, "vg_uuid": vg_uuid, "cat_key": cat_key, "cat_val": cat_val, "cat_uuid": cat_uuid})

  """
  vg_index = 1
  for i in range(11, 21):
    cat_key = "cat-" + str(i)
    cat_val = "val-" + str(i)
    cat_uuid = cat_key_uuid_map[cat_key]
    for i in range(10):
      vg_name_list = ["vg-b-" + str(vg_index), "vg-b-" + str(vg_index+100)]
      vg_index += 1
      for vg_name in vg_name_list:
        if vg_name not in vgs:
          continue
        vg_uuid = vg_name_uuid_map[vg_name]
        vg_category_list.append({"vg_name": vg_name, "vg_uuid": vg_uuid, "cat_key": cat_key, "cat_val": cat_val, "cat_uuid": cat_uuid})
  """
  return vg_category_list

def add_cat(vg_category_list):
  for i in vg_category_list:
    vg_name = i["vg_name"]
    vg_uuid = i["vg_uuid"]
    cat_key = i["cat_key"]
    cat_val = i["cat_val"]
    cat_uuid = i["cat_uuid"]
    v = vg_obj.get(vg_uuid=vg_uuid)
    already_added_category_uuid_list = [i["extId"] for i in v.category_list]
    if cat_uuid in already_added_category_uuid_list:
      print "VG: {0} - {1} already has category: ({2}, {3})".format(vg_name, vg_uuid, cat_key, cat_val)
      continue
    print "VG: {0} - {1} adding category: ({2}, {3})".format(vg_name, vg_uuid, cat_key, cat_val)
    v.add_category(cat_uuid=cat_uuid)
    

if __name__=="__main__":
  vg_category_list = get_vg_category_list()
  #print vg_category_list
  add_cat(vg_category_list)

import sys
from framework.vm_entity import VM
from framework.vg_entity import VG
from framework.cg_entity import CG
from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
#IP = SRC_PC_IP

vg = VG(IP)
cg = CG(IP)
vm = VM(IP)
cat = Category(IP)

cg_obj = cg.get(cg_name=sys.argv[1])

cluster_list = list()
category_list = list()

for v in cg_obj.vg_list:
  _v = vg.get(vg_uuid=v)
  print "#####"
  print "VG-NAME: {0}, VG-UUID: {1}".format(_v.name, _v.uuid)
  print "VG is on cluster: {0}".format(_v.cluster)

  if _v.cluster not in cluster_list:
    cluster_list.append(_v.cluster)

  cat_list = _v.get_categories()
  for i in cat_list:
    cat_uuid = i["extId"]

    if cat_uuid not in category_list:
      category_list.append(cat_uuid)

    _c = cat.get(cat_uuid=cat_uuid) 
    print "CAT_KEY: {0}, CAT_VAL: {1}, CAT_UUID: {2}".format(_c.cat_key, _c.cat_val, cat_uuid)
  print "#####\n"

for v in cg_obj.vm_list:
  _v = vm.get(vm_uuid=v)
  print "#####"
  print "VM-NAME: {0}, VM-UUID: {1}".format(_v.name, _v.uuid)
  print "VM is on cluster: {0}".format(_v.cluster_uuid)

  if _v.cluster_uuid not in cluster_list:
    cluster_list.append(_v.cluster_uuid)

  cat_mapping = _v.get_categories()
  for i in cat_mapping:
    #cat_key = i
    #cat_val = cat_mapping[i][0]
    _c = cat.get(cat_key=i, cat_val=cat_mapping[i][0]) 

    if _c.uuid not in category_list:
      category_list.append(_c.uuid)

    print "CAT_KEY: {0}, CAT_VAL: {1}, CAT_UUID: {2}".format(_c.cat_key, _c.cat_val, _c.uuid)
  print "#####\n"


print cluster_list
print category_list

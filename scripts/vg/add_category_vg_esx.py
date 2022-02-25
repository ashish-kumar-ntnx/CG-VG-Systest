from framework.vg_entity import VG
from framework.category_entity import Category
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

SRC_PC_IP = "10.40.216.116"
v = VG(SRC_PC_IP)
c = Category(SRC_PC_IP)
"""
cat_vg_list = [
  {"vg_list": ["vg-1", "vg-2"], "cat_key": "cat-1", "cat_val": "val-1"},
  {"vg_list": ["vg-3", "vg-4"], "cat_key": "cat-2", "cat_val": "val-2"},
  {"vg_list": ["vg-5", "vg-6"], "cat_key": "cat-3", "cat_val": "val-3"},
  {"vg_list": ["vg-7", "vg-8"], "cat_key": "cat-4", "cat_val": "val-4"},
]
"""
cat_vg_list = [
  {"vg_list": ['ak-vg-1', 'ak-vg-2', 'ak-vg-3', 'ak-vg-4', 'ak-vg-5', 'ak-vg-6', 'ak-vg-7', 'ak-vg-8', 'ak-vg-9', 'ak-vg-10', 'ak-vg-11', 'ak-vg-12', 'ak-vg-13', 'ak-vg-14', 'ak-vg-15', 'ak-vg-16', 'ak-vg-17', 'ak-vg-18', 'ak-vg-19', 'ak-vg-20'], "cat_key": "ak-cat", "cat_val": "ak-val"}
]

for i in cat_vg_list:
  vg_list = i["vg_list"]
  cat_key = i["cat_key"]
  cat_val = i["cat_val"]
  for j in vg_list:
    print "Attaching category: ({0}, {1}) to VG: {2}".format(cat_key, cat_val, j)
    vg = v.get(vg_name=j)
    vg.add_category(cat_key, cat_val)

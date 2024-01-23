from framework.category_entity import Category
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = SRC_PC_IP
#IP = TGT_PC_IP
cat_obj = Category(IP)
#cat_obj = Category("10.40.184.111")
for i in range(1, 17):
  #cat_key, cat_val = "vdi_cat_" + str(i), "vdi_val_" + str(i)
  cat_key, cat_val = "cat-" + str(i), "val-" + str(i)
  #cat_key, cat_val = "self-az-cat-" + str(i), "val-" + str(i)
  #cat_key, cat_val = "scale-cat-" + str(i), "scale-val-" + str(i)
  print "Creating category {0}: {1}".format(cat_key, cat_val)
  cat_obj.create(cat_key, cat_val)

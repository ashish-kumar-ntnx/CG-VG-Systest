import time
from framework.image_entity import Image
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE, PROTECTION_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM                          
elif SETUP_TYPE == "AHV":                                           
  from framework.vm_entity import VM

IP = TGT_PC_IP
IP = SRC_PC_IP

START = 1
END = 1001
vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
#print vm_name_uuid_map

#vm_name_list = ["vm-" + str(i) for i in range(111, 131)]
vm_name_list = ["vm-" + str(i) for i in range(START, END)]

def get_vm_category_list():
  vm_category_list = list()
  vm_index = 1
  for i in range(1, 11):
    if PROTECTION_TYPE == "category":
      #cat_key = "self-az-cat-" + str(i)
      cat_key = "scale-cat-" + str(i)
      cat_val = "scale-val-" + str(i)
    elif PROTECTION_TYPE == "explicit":
      cat_key = "ProtectionRule" 
      cat_val = "pr-" + str(i)
    for _ in range(100):
      vm_name = "vm-scale-" + str(vm_index)
      vm_index += 1
      #if vm_name not in vm_name_list:
      if vm_name not in vm_name_uuid_map:
        continue
      vm_uuid = vm_name_uuid_map[vm_name]
      vm_category_list.append({"vm_name": vm_name, "vm_uuid": vm_uuid, "cat_key": cat_key, "cat_val": cat_val})
  return vm_category_list

def add_cat(vm_category_list):
  for i in vm_category_list:
    vm_name = i["vm_name"]
    vm_uuid = i["vm_uuid"]
    cat_key = i["cat_key"]
    cat_val = i["cat_val"]
    v = vm_obj.get(vm_uuid=vm_uuid)
    #v.remove_category()
    #time.sleep(1)
    already_added_categories = v.get_categories().keys()
    if cat_key in already_added_categories:
      print "VM: {0} - {1} already has category: ({2}, {3})".format(vm_name, vm_uuid, cat_key, cat_val)
      continue
    print "VM: {0} - {1} adding category: ({2}, {3})".format(vm_name, vm_uuid, cat_key, cat_val)
    v.attach_category(cat_key=cat_key, cat_val=cat_val)
    

if __name__=="__main__":
  vm_category_list = get_vm_category_list()
  #print vm_category_list
  add_cat(vm_category_list)

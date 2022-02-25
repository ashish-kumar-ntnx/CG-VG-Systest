from pprint import pprint
vm_dict = dict()

END = 201
CLUSTER_GAP = 100
IMAGE_GAP = 15
CATEGORY_GAP = 10
CONTAINER_GAP = 10

# Base VM dict
for i in range(1, END):
  tmp = dict()
  tmp["name"] = "vm-" + str(i)
  tmp["disk_size_bytes"] = 5368709120
  tmp["nic"] = "vlan0"
  vm_dict[tmp["name"]] = tmp

# Update cluster name
clus_num = 0
for i in range(1, END, CLUSTER_GAP):
  clus_num += 1
  cluster_name = "PC-A-PE-" + str(clus_num)
  for j in range(i, i + CLUSTER_GAP):
    vm_name = "vm-" + str(j)
    vm_dict[vm_name]["cluster"] = cluster_name 
    
# Update image name
image_list = ["rhel_77", "rhel_76", "rhel_74", "rhel_73", "rhel_72", "rhel_69", "rhel_68", "rhel_67", "oel_69", "oel_77", "centos_72", "sles11_sp4", "sles12_sp4", "win2019_server", "win2016_server", "win2012r2_server", "win2008r2_server"]
image_index = 0
for i in range(1, END, IMAGE_GAP):
  image = image_list[image_index]
  image_index += 1
  for j in range(i, i + IMAGE_GAP):
    if j == END:
      break
    vm_name = "vm-" + str(j)
    vm_dict[vm_name]["image"] = image

# Update category
cat_num = 0
for i in range(1, END, CATEGORY_GAP):
  cat_num += 1
  cat_key = "cat-" + str(cat_num)
  cat_val = "val-" + str(cat_num)
  for j in range(i, i + CLUSTER_GAP):
    if j == END:
      break
    vm_name = "vm-" + str(j)
    vm_dict[vm_name]["cat_key"] = cat_key
    vm_dict[vm_name]["cat_val"] = cat_val

# Update container name
ctr_num = 0
for i in range(1, END, CONTAINER_GAP):
  ctr_num += 1
  ctr_name = "cg-vg-ctr-" + str(ctr_num)
  for j in range(i, i + CLUSTER_GAP):
    if j == END:
      break
    vm_name = "vm-" + str(j)
    vm_dict[vm_name]["ctr"] = ctr_name

#pprint(vm_dict)

# Update DB
from tinydb import TinyDB, Query
DB = TinyDB("../db/vm_small_spec.json")
for vm in vm_dict:
  DB.insert({"name": vm, "spec": vm_dict[vm]})

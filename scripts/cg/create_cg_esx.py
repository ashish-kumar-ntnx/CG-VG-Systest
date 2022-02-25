from framework.cg_entity import CG
from framework.mh_vm_entity import VM
from framework.vg_entity import VG
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

SRC_PC_IP = "10.40.216.116"
cg = CG(SRC_PC_IP)
vm = VM(SRC_PC_IP)
vg = VG(SRC_PC_IP)

cg_map = {
  "ak-cg-1":
  {
    "vm_name_list": ["ak-vm-1", "ak-vm-2", "ak-vm-3", "ak-vm-4", "ak-vm-5", "ak-vm-6", "ak-vm-7", "ak-vm-8", "ak-vm-9", "ak-vm-10"],
    "vg_name_list": ['ak-vg-1', 'ak-vg-2', 'ak-vg-3', 'ak-vg-4', 'ak-vg-5', 'ak-vg-6', 'ak-vg-7', 'ak-vg-8', 'ak-vg-9', 'ak-vg-10', 'ak-vg-11', 'ak-vg-12', 'ak-vg-13', 'ak-vg-14', 'ak-vg-15', 'ak-vg-16', 'ak-vg-17', 'ak-vg-18', 'ak-vg-19', 'ak-vg-20']
  }
}

#cg_map = {
#  "cg-1":
#  {
#    "vm_name_list": ["vm-1", "vm-2"],
#    "vg_name_list": ["vg-1", "vg-2", "vg-3", "vg-4"]
#  },
#  "cg-2":
#  {
#    "vm_name_list": ["vm-3", "vm-4"],
#    "vg_name_list": ["vg-5", "vg-6", "vg-7", "vg-8"]
#  }
#}

vm_name_uuid_map = vm.get_name_uuid_map()
vg_name_uuid_map = vg.get_name_uuid_map()
#print vm_name_uuid_map

for cg_name in cg_map:
  vm_name_list = cg_map[cg_name]["vm_name_list"]
  vg_name_list = cg_map[cg_name]["vg_name_list"]
  print "Creating CG: {0}, vm_list: {1}, vg_list: {2}".format(cg_name, vm_name_list, vg_name_list)
  vm_list = [vm_name_uuid_map[i] for i in vm_name_list]
  vg_list = [vg_name_uuid_map[i] for i in vg_name_list]
  cg.create(cg_name, vm_list, vg_list)
  
"""  

def create_cg():
  cg_new_obj_list = list()
  vm_num = 1
  for i in range(1, 21):
    cg_name = "cg-" + str(i)
    vm_list = []
    vg_list = []

    for i in range(10):
      vm_name = "vm-" + str(vm_num)
      vm_num += 1

      q = Query()
      vm_list.append(vm_db.search(q.name == vm_name)[0]["uuid"])
      q = Query()
      vg_list.append(vg_db.search(q.name == vg_a_name)[0]["uuid"])
      vg_list.append(vg_db.search(q.name == vg_b_name)[0]["uuid"])

      vg_a_name = "vg-a-" + str(vm_num)
      vg_b_name = "vg-b-" + str(vm_num)

    cg_spec = dict()
    cg_spec["name"] = cg_name
    cg_spec["members"] = list()

    for vm in vm_list:
      tmp = dict()
      tmp["entityType"] = "VM"
      tmp["extId"] = vm
      cg_spec["members"].append(tmp)

    for vg in vg_list:
      tmp = dict()
      tmp["entityType"] = "VOLUME_GROUP"
      tmp["extId"] = vg
      cg_spec["members"].append(tmp)

    print "Creating CG: {0} ...".format(cg_name)
    
    cg_tmp = cg_obj.create(cg_name, vm_list, vg_list)
    cg_new_obj_list.append(cg_tmp)
    return cg_new_obj_list

def check_status_of_cg(cg_new_obj_list):
  for cg_new in cg_new_obj_list:
    tmp = cg_new.get(cg_uuid=cg_new.uuid)
    print tmp.name, tmp.uuid

if __name__=="__main__":
  cg_new_obj_list = create_cg()
  check_status_of_cg(cg_new_obj_list)
""" 

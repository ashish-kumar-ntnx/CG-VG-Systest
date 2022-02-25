from framework.recovery_plan_entity import RecoveryPlan
from framework.vm_entity import VM
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
cg = CG(IP)
vm = VM(IP)
vg = VG(IP)



vm_num = 1
vg_num_a = 1
vg_num_b = 1

vm_name_uuid_map = vm.get_name_uuid_map()
vg_name_uuid_map = vg.get_name_uuid_map()
#print vm_name_uuid_map

for i in range(1, 21):
  cg_name = "cg-" + str(i)
  pe_name = "PC-A-PE-1" if i < 11 else "PC-A-PE-1"
  vg_prefix= "vg-a-" if i < 11 else "vg-b-"

  vm_name_list, vg_name_list = [], []
  vm_list, vg_list = [], []
  for j in range(10):
    vm_name = "vm-" + str(vm_num)
    vm_name_list.append(vm_name)
    vm_list.append(vm_name_uuid_map[vm_name])
    vm_num += 1

    if vg_prefix == "vg-a-":
      vg_name = vg_prefix + str(vg_num_a)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_name = vg_prefix + str(vg_num_a + 100)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_num_a += 1
    else:
      vg_name = vg_prefix + str(vg_num_b)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_name = vg_prefix + str(vg_num_b + 100)
      vg_name_list.append(vg_name)
      vg_list.append(vg_name_uuid_map[vg_name])
      vg_num_b += 1

  print "Creating CG: {0}, with vms: {1}, vgs: {2}".format(cg_name, vm_name_list, vg_name_list)
  cg.create(cg_name, vm_list, vg_list)
  #print cg_name
  #print vm_name_list
  #print vg_name_list
  #print vm_list
  #print vg_list
  print "\n"
  
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

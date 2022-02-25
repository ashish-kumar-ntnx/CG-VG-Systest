from pprint import pprint
from framework.vg_entity import VG
#from framework.vm_entity import VM
from framework.vm_entity import VM
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
vm_obj = VM(IP)
vg_obj = VG(IP)

vg_name_uuid_map = vg_obj.get_name_uuid_map()
vm_name_uuid_map = vm_obj.get_name_uuid_map()

START = 1
END = 10

def get_attached_vms(vm_iqn_map):
  for i in range(START, END):
    vg_name_list = ["vg-a-" + str(i), "vg-b-" + str(i)]
    for vg_name in vg_name_list:
      vg_uuid = vg_name_uuid_map[vg_name]
      vg = vg_obj.get(vg_uuid=vg_uuid)
      iscsi_client_list = vg.get_iscsi_attachments()
      vm_iqn_list = list()
      iscsi_init_list = list()
      for i in iscsi_client_list:
        iqn = i["iscsiInitiatorName"]
        t = dict()
        t["iqn"] = iqn
        t["vm_name"] = vm_iqn_map[iqn]["vm_name"]
        t["vm_uuid"] = vm_iqn_map[iqn]["vm_uuid"]
        vm_iqn_list.append(t)
        #iscsi_init_list.append(i["iscsiInitiatorName"])
      print "\n#######"
      print "For VG: {0} - {1}".format(vg_name, vg_uuid)
      print "Attached VM List: {0}".format(vm_iqn_list)
      #print "Attached iscsi clients: {0}".format(iscsi_init_list)
      #print "Attached vms: {0}".format(vm_iqn_map)
      print "#######\n"

def get_vm_iqn_map():
  vm_iqn_map = {}
  for i in range(START, END):
    vm_name = "vm-" + str(i)
    vm_uuid = vm_name_uuid_map[vm_name]
    vm = vm_obj.get(vm_uuid=vm_uuid)
    iqn = vm.get_iqn()
    vm_iqn_map[iqn] = {"vm_name": vm_name, "vm_uuid": vm_uuid}
  #print vm_iqn_map
  return vm_iqn_map

if __name__=="__main__":
  vm_iqn_map = get_vm_iqn_map()
  get_attached_vms(vm_iqn_map)  
    

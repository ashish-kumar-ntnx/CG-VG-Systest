from pprint import pprint
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
import time
import threading
ENABLE_CLIENT_CHAP = True

def get_vm_vg_list(CLUS_LIST):
  vm_vg_list = list()
  #vm_pre = "DB-VM-"
  #vg_a = "DB-VG-"
  vm_pre = "vm-"
  vg_a = "vg-a-"
  vg_b = "vg-b-"

  vg_index = 1
  vg_index = 1
  for i in range(1, 55):
    vg_pre = "vg-a-"
    #vg_pre = "DB-VG-"
    cluster_name = CLUS_LIST[0] 
    tmp = dict()
    tmp["vm_name"] = vm_pre + str(i)
    tmp["cluster_name"] = cluster_name
    tmp["vg_list"] = list()
    tmp["vg_list"].append({"attach_type": "iscsi", "vg_name": vg_pre + str(vg_index)})
    tmp["vg_list"].append({"attach_type": "iscsi", "vg_name": vg_pre + str(vg_index + 100)})
    vg_index += 1
    vm_vg_list.append(tmp)
    
  return vm_vg_list

def do_attachment(vm_vg_map, VM_OBJ, VG_OBJ, vm_name_uuid_map, vg_name_uuid_map):

  vm_name = vm_vg_map["vm_name"]
  cluster_name = vm_vg_map["cluster_name"]
  vg_list = vm_vg_map["vg_list"]
  vm_uuid = vm_name_uuid_map[vm_name]
  vm1 = VM_OBJ.get(vm_uuid=vm_uuid)
  vm1.enable_iscsi()
  vm1.generate_new_iqn()
  vm1.get_iqn()
  vm_attach_spec = {"iscsiInitiatorName": vm1.iqn}
  if ENABLE_CLIENT_CHAP:
    vm_attach_spec["clientSecret"] = "Nutanix.1234"
    vm_attach_spec["enabledAuthentications"] = "CHAP"
  #print vm_attach_spec
  for vg in vg_list:
    attach_type = vg["attach_type"]
    vg_name = vg["vg_name"]
    print "Attaching VG: {0} to VM: {1} with attach_type: {2}".format(vg_name, vm_name, attach_type)
    #vg1 = VG_OBJ.get(vg_name=vg_name)
    vg1 = VG_OBJ.get(vg_uuid=vg_name_uuid_map[vg_name])
    current_iqn_attachments = list()
    if vg1.iscsi_attachment_list:
      current_iqn_attachments = [i["iscsiInitiatorName"]for i in vg1.iscsi_attachment_list]
    #print "ci: {0}".format(current_iqn_attachments)
    #print "vi: {0}".format(vm1.iqn)
    if attach_type == "iscsi":
      #print vm1.iqn, current_iqn_attachments[0]
      if vm1.iqn in current_iqn_attachments:
        print "VM IQN: {0} already attached to VG: {1}".format(vm1.iqn, vg1.name)
        continue
      #print "Current iscsi_attachment: {0}".format(vg1.iscsi_attachment_list)
      
      attach_task_url = vg1.attach_iscsi(vm_attach_spec)
      print attach_task_url
      #new_iscsi_attachments = vg1.get_iscsi_attachments()
      #print new_iscsi_attachments
    elif attach_type == "hyp":
      print "Hyp attachment not supported yet!!!"


if __name__=="__main__":

  on_tgt = False
  #on_tgt = True
  if on_tgt:
    IP = TGT_PC_IP
    CLUS_LIST = TGT_CLUS_LIST
  else:
    IP = SRC_PC_IP
    #IP = "10.33.128.61"
    CLUS_LIST = SRC_CLUS_LIST
    
  vm_vg_list = get_vm_vg_list(CLUS_LIST)
  pprint(vm_vg_list)

  VM_OBJ = VM(IP)
  VG_OBJ = VG(IP)
  vm_name_uuid_map = VM_OBJ.get_name_uuid_map()
  vg_name_uuid_map = VG_OBJ.get_name_uuid_map()

  for i in range(0, len(vm_vg_list), 4):
    threads = list()
    for j in range(i, i+4):
      x = threading.Thread(target=do_attachment, args=(vm_vg_list[j], VM_OBJ, VG_OBJ, vm_name_uuid_map, vg_name_uuid_map,))
      threads.append(x)
    for th in threads:
      th.start()
    for th in threads:
      th.join()

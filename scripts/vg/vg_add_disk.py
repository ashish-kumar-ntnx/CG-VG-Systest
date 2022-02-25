import time
import random
from pprint import pprint
#from vg_spec_generator import generate_vg_spec
from framework.vg_entity import VG
from framework.ctr_entity import Ctr
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
PE_1 = TGT_CLUS_LIST[0]
#IP = SRC_PC_IP
#PE_1 = SRC_CLUS_LIST[0]
#PE_2 = TGT_CLUS_LIST[1]

c = Ctr(IP)
vg = VG(IP)
FINAL_DISK_COUNT = 10

vg_name_uuid_map = vg.get_name_uuid_map()
#print vg_name_uuid_map
disk_size_range = [1, 3]

def add_disk_for_pe_1():
  PE_1_CTR_UUID_LIST = []
  pe_1_ctr_name_uuid_map = c.get_name_uuid_map(cluster_name=PE_1)
  for ctr_name in pe_1_ctr_name_uuid_map:
    if ctr_name.startswith("cg-vg-ctr"):
      PE_1_CTR_UUID_LIST.append(pe_1_ctr_name_uuid_map[ctr_name])

  for i in range(1, 201):
    vg_name = "vg-a-" + str(i)
    vg_uuid = vg_name_uuid_map[vg_name]
    vg_obj = vg.get(vg_uuid=vg_uuid)
    disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
    num_disks = len(disk_uuid_list)
    disk_spec_list = list()
    if num_disks < FINAL_DISK_COUNT:
      print "**** For VG: {0} - {1}, disk_count: {2}".format(vg_name, vg_uuid, num_disks)
      num_disks_to_add = FINAL_DISK_COUNT - num_disks
      print "Adding {0} disks to VG: {1}".format(num_disks_to_add, vg_name)
      #print "Generating disk specs."
      tmp = dict()
      for i in range(num_disks_to_add):
        disk_size = random.choice(disk_size_range)
        ctr_uuid = random.choice(PE_1_CTR_UUID_LIST)
        tmp["diskSizeBytes"] = disk_size * 1024 * 1024 * 1024
        tmp["diskDataSourceReference"] = {"extId": ctr_uuid, "entityType": "STORAGE_CONTAINER"}
        disk_spec_list.append(tmp)
      #print disk_spec_list
      for disk_spec in disk_spec_list:
        vg.add_disk(disk_spec=disk_spec)
      
def add_disk_for_pe_2():
  PE_2_CTR_UUID_LIST = []
  pe_2_ctr_name_uuid_map = c.get_name_uuid_map(cluster_name=PE_2)
  for ctr_name in pe_2_ctr_name_uuid_map:
    if ctr_name.startswith("cg-vg-ctr"):
      PE_2_CTR_UUID_LIST.append(pe_2_ctr_name_uuid_map[ctr_name])

  for i in range(1, 201):
    vg_name = "vg-b-" + str(i)
    vg_uuid = vg_name_uuid_map[vg_name]
    vg_obj = vg.get(vg_uuid=vg_uuid)
    disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
    num_disks = len(disk_uuid_list)
    disk_spec_list = list()
    if num_disks < FINAL_DISK_COUNT:
      print "**** For VG: {0} - {1}, disk_count: {2}".format(vg_name, vg_uuid, num_disks)
      num_disks_to_add = FINAL_DISK_COUNT - num_disks
      print "Adding {0} disks to VG: {1}".format(num_disks_to_add, vg_name)
      #print "Generating disk specs."
      tmp = dict()
      for i in range(num_disks_to_add):
        disk_size = random.choice(disk_size_range)
        ctr_uuid = random.choice(PE_2_CTR_UUID_LIST)
        tmp["diskSizeBytes"] = disk_size * 1024 * 1024 * 1024
        tmp["diskDataSourceReference"] = {"extId": ctr_uuid, "entityType": "STORAGE_CONTAINER"}
        disk_spec_list.append(tmp)
      for disk_spec in disk_spec_list:
        vg.add_disk(disk_spec=disk_spec)

if __name__=="__main__":
  add_disk_for_pe_1()
  #add_disk_for_pe_2()

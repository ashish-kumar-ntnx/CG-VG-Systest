import sys
import time
from pprint import pprint
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, DEFAULT_CHAP_PASSWORD
import random

IP = SRC_PC_IP
#IP = TGT_PC_IP
vg = VG(IP)
OP_INTERVAL = 5
CTR_UUID = "978e45e8-b0d9-44e1-91a0-b49aa7b64a98"
#CTR_UUID = "b254b61c-1d07-402d-979f-5e3b07fca325"
vg_name_uuid_map = vg.get_name_uuid_map()

def add_chap(vg_name):
  print "Adding CHAP to VG: {0}".format(vg_name)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj=vg.get(vg_uuid=vg_uuid)
  vg_obj.add_chap(DEFAULT_CHAP_PASSWORD)

def remove_chap(vg_name):
  print "Removing CHAP from VG: {0}".format(vg_name)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj=vg.get(vg_uuid=vg_uuid)
  vg_obj.remove_chap()

def add_disk(vg_name):
  disk_size_range = [1, 3]
  print "Adding disk to VG: {0}".format(vg_name)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj=vg.get(vg_uuid=vg_uuid)
  disk_spec = dict()
  disk_size = random.choice(disk_size_range)
  disk_spec["diskSizeBytes"] = disk_size * 1024 * 1024 * 1024
  disk_spec["diskDataSourceReference"] = {"extId": CTR_UUID, "entityType": "STORAGE_CONTAINER"}
  vg_obj.add_disk(disk_spec=disk_spec)

def remove_disk(vg_name):
  print "Removing disk from VG: {0}".format(vg_name)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj=vg.get(vg_uuid=vg_uuid)
  disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
  disk_uuid = disk_uuid_list[-1]
  vg_obj.remove_disk(disk_uuid)

def change_name(vg_name, new_name):
  print "Renaming VG: {0} to name: {1}".format(vg_name, new_name)
  vg_uuid = vg_name_uuid_map[vg_name]
  vg_obj=vg.get(vg_uuid=vg_uuid)
  vg_obj.update_name(new_name)
  time.sleep(OP_INTERVAL)
  print "Renaming VG: {0} to name: {1}".format(new_name, vg_name)
  vg_obj.update_name(vg_name)
  

for i in range(1, 101):
  print "\n#### Iteration-{0} ####\n".format(i)
  op_type = random.randint(1, 3)
  #vg_id_1 = random.randint(1, 160)
  vg_id_1 = random.randint(1, 100)
  vg_name = "vdi-vm-{0}-vg-1".format(vg_id_1)
  if op_type == 1:
    add_chap(vg_name)
    time.sleep(OP_INTERVAL)
    remove_chap(vg_name)
  elif op_type == 2:
    add_disk(vg_name)
    time.sleep(OP_INTERVAL)
    remove_disk(vg_name)
  elif op_type == 3:
    change_name(vg_name, "{0}-new".format(vg_name))
  else:
    continue

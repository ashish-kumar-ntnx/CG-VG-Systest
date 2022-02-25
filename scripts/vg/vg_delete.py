import sys
import time
from pprint import pprint
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time
import threading

IP = SRC_PC_IP
IP = TGT_PC_IP
vg = VG(IP)

vg_name_uuid_map = vg.get_name_uuid_map()


print "Deleting VGs on {0}, do you want to continue:(Y/N)".format(IP)
if raw_input("=> ").lower() != "y":
  sys.exit(1)

def del_vg(vg_name):
    if vg_name not in vg_name_uuid_map:
      return
    vg_uuid = vg_name_uuid_map[vg_name]
    vg_obj=vg.get(vg_uuid=vg_uuid)
    #print "\n######"
    #disk_uuid_list = [i["extId"] for i in vg_obj.disk_list]
    #print "VG: {0} - {1}, disk_len: {2}".format(vg_name, vg_uuid, len(disk_uuid_list))
    #if len(disk_uuid_list) != 11:
    #if vg_obj.cluster != "0005c6fe-1e48-3c4e-3045-ac1f6b15d8c2":
    #  continue
    print "Deleting VG: {0} - {1}".format(vg_name, vg_uuid)
    #print len(disk_uuid_list)
    print "Removing iscsi_attachments."
    iscsi_client_list = vg_obj.get_iscsi_attachments()
    for i in iscsi_client_list:
      print vg_obj.detach_iscsi(i["extId"])
    out = vg_obj.remove()
    print "Delete Task UUID: {0}".format(out)
    print "######\n"


vg_prefix = "vg-a-"
START, END = 1, 201
for i in range(START, END, 4):
  threads = list()
  for j in range(i, i+4):
    vg_name = vg_prefix + str(j)
    x = threading.Thread(target=del_vg, args=(vg_name,))
    threads.append(x)
  for th in threads:
    th.start()
  for th in threads:
    th.join()

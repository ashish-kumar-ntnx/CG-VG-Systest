import sys
import time
from pprint import pprint
from framework.vg_entity import VG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = SRC_PC_IP
#IP = TGT_PC_IP
vg = VG(IP)

vg_name_uuid_map = vg.get_name_uuid_map()

#vg_name = sys.argv[1]
#vg_uuid = vg_name_uuid_map[vg_name]
#vg_obj=vg.get(vg_uuid=vg_uuid)
#print "\n######"
#print "Deleting VG: {0} - {1}".format(vg_name, vg_uuid)
#print "Removing iscsi_attachments."
#iscsi_client_list = vg_obj.get_iscsi_attachments()
#for i in iscsi_client_list:
#  print vg_obj.detach_iscsi(i["extId"])
#out = vg_obj.remove()
#print "Delete Task UUID: {0}".format(out)
#print "######\n"



#for i in range(1, 11):
for i in range(1, 101):
  #vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i), "vg-b-" + str(i), "vg-b-" + str(100 + i)]
  vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i)]
  #vg_name_list = ["vg-b-" + str(i), "vg-b-" + str(100 + i)]
  for vg_name in vg_name_list:
    if vg_name in vg_name_uuid_map:
    #if vg_name in ["vg-a-20", "vg-a-120"]:
      vg_uuid = vg_name_uuid_map[vg_name]
      vg_obj=vg.get(vg_uuid=vg_uuid)
      #print "\n######"
      print "Removing iscsi_attachments from VG: {0} - {1}".format(vg_name, vg_uuid)
      iscsi_client_list = vg_obj.get_iscsi_attachments()
      for i in iscsi_client_list:
        print vg_obj.detach_iscsi(i["extId"])
      print "######\n"

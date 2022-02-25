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

print "Deleting VGs on {0}, do you want to continue:(Y/N)".format(IP)
if raw_input("=> ").lower() != "y":
  sys.exit(1)
"""
for vg_name in vg_name_uuid_map:
  if vg_name.startswith("nutest"):
    vg_uuid = vg_name_uuid_map[vg_name]
    vg_obj=vg.get(vg_uuid=vg_uuid)
    print "Deleting VG: {0} - {1}".format(vg_name, vg_uuid)
    #print len(disk_uuid_list)
    print "Removing iscsi_attachments."
    iscsi_client_list = vg_obj.get_iscsi_attachments()
    for i in iscsi_client_list:
      print vg_obj.detach_iscsi(i["extId"])
    out = vg_obj.remove()
    print "Delete Task UUID: {0}".format(out)
    print "######\n"

"""
#vg_prefix_list = ["vg-a-", "vg-b-"]
#vg_prefix_list = ["Nutanix-Test-vg-a-"]
vg_prefix_list = ["vg-a-"]
START, END = 1, 201
for i in range(START, END):
  vg_name_list = [j + str(i) for j in vg_prefix_list]
  #vg_name_list.extend([j + str(i+100) for j in vg_prefix_list])
  #vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i), "vg-b-" + str(i), "vg-b-" + str(100 + i)]
  #vg_name_list = ["vg-a-" + str(i), "vg-a-" + str(100 + i), "vg-b-" + str(i), "vg-b-" + str(100 + i)]
  for vg_name in vg_name_list:
    if vg_name in vg_name_uuid_map:
      print vg_name
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

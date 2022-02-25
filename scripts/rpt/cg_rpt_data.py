import sys
from framework.cg_entity import CG
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#SRC_IP = TGT_PC_IP
#TGT_IP = SRC_PC_IP
SRC_IP = SRC_PC_IP
TGT_IP = TGT_PC_IP

#SRC_IP, TGT_IP = "10.40.216.116", "10.40.216.116"


if len(sys.argv) not in [2, 3]:
  print "\n\tUsage: python cg_rpt_data.py <cg_name>\n\tOR"
  print "\tUsage: python cg_rpt_data.py <cg_name> <details>\n"
  sys.exit(1)
cg_name = sys.argv[1]

get_details = False
if len(sys.argv) == 3:
   get_details = True

cg_obj = CG(SRC_IP)
src_rpt_obj = RecoveryPoint(SRC_IP)
rmt_rpt_obj = RecoveryPoint(TGT_IP)

def get_rpt_details(rpt_uuid_list, source=True):
  if source:
    rpt_obj = src_rpt_obj
  else:
    rpt_obj = rmt_rpt_obj
  for rpt_uuid in rpt_uuid_list:
    print "\nBase RPT: {0}".format(rpt_uuid)
    rpt = rpt_obj.get(rpt_uuid)
    print "  RPT UUID: {0}".format(rpt.uuid)
    print "  RPT NAME: {0}".format(rpt.name)
    print "  RPT LAU: {0}".format(rpt.loc_agn_uuid)
    print "  RPT CreationTime: {0}".format(rpt.creation_time)
    print "  RPT ExpiryTime: {0}".format(rpt.expiry_time)
    print "  RPT Status: {0}".format(rpt.status)
    print "  RPT RecoveryPointType: {0}\n".format(rpt.rp_type)
    for vm_rpt in rpt.vm_rpt_list:
      print "    VM RPT UUID: {0}".format(vm_rpt.uuid)
      print "    VM RPT NAME: {0}".format(vm_rpt.name)
      print "    VM RPT LAU: {0}".format(vm_rpt.loc_agn_uuid)
      print "    VM RPT CreationTime: {0}".format(vm_rpt.creation_time)
      print "    VM RPT ExpiryTime: {0}".format(vm_rpt.expiry_time)
      print "    VM RPT Status: {0}".format(vm_rpt.status)
      print "    VM RPT RecoveryPointType: {0}\n".format(vm_rpt.rp_type)
      for disk_rpt in vm_rpt.vm_disk_rpt_list:
        print "      VM DISK RPT UUID: {0}".format(disk_rpt.uuid)
        print "      VM DISK RPT NAME: {0}".format(disk_rpt.name)
        print "      VM DISK RPT LAU: {0}".format(disk_rpt.loc_agn_uuid)
        print "      VM DISK RPT CreationTime: {0}".format(disk_rpt.creation_time)
        print "      VM DISK RPT ExpiryTime: {0}".format(disk_rpt.expiry_time)
        print "      VM DISK RPT Status: {0}".format(disk_rpt.status)
        print "      VM DISK RPT RecoveryPointType: {0}\n".format(disk_rpt.rp_type)
    for vg_rpt in rpt.vg_rpt_list:
      print "    VG RPT UUID: {0}".format(vg_rpt.uuid)
      print "    VG RPT NAME: {0}".format(vg_rpt.name)
      print "    VG RPT LAU: {0}".format(vg_rpt.loc_agn_uuid)
      print "    VG RPT CreationTime: {0}".format(vg_rpt.creation_time)
      print "    VG RPT ExpiryTime: {0}".format(vg_rpt.expiry_time)
      print "    VG RPT Status: {0}".format(vg_rpt.status)
      print "    VG RPT RecoveryPointType: {0}\n".format(vg_rpt.rp_type)
      for disk_rpt in vg_rpt.vg_disk_rpt_list:
        print "      VG DISK RPT UUID: {0}".format(disk_rpt.uuid)
        print "      VG DISK RPT NAME: {0}".format(disk_rpt.name)
        print "      VG DISK RPT LAU: {0}".format(disk_rpt.loc_agn_uuid)
        print "      VG DISK RPT CreationTime: {0}".format(disk_rpt.creation_time)
        print "      VG DISK RPT ExpiryTime: {0}".format(disk_rpt.expiry_time)
        print "      VG DISK RPT Status: {0}".format(disk_rpt.status)
        print "      VG DISK RPT RecoveryPointType: {0}\n".format(disk_rpt.rp_type)

cg = cg_obj.get(cg_name=cg_name)
print "Finding all the recovery_points of the CG: {0} - {1}".format(cg_name, cg.uuid)
vm_live_entity_uuid_list = "|".join(cg.vm_list)
disk_group_live_entity_uuid_list = "|".join(cg.vg_list)

filter_criteria = {
  "entity_type":"recovery_point",
  "group_member_sort_attribute": "_created_timestamp_usecs_",
  "group_member_sort_order": "DESCENDING",
  "group_member_attributes": 
  [
    {
      "attribute": "_created_timestamp_usecs_"
    }
  ],
  "filter_criteria":"vm_live_entity_uuid_list=={0};disk_group_live_entity_uuid_list=={1}".format(vm_live_entity_uuid_list, disk_group_live_entity_uuid_list)
}
#print filter_criteria
out = src_rpt_obj.get_groups_response(filter_criteria)
rpt_uuid_list = list()
if out["filtered_group_count"] > 0:
  rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
  if get_details:
    print "\nGetting RPT details on Source.\n"
    get_rpt_details(rpt_uuid_list)
  else:
    #print "\nFound RecoveryPoints on Source:\n{0}".format("\n".join(rpt_uuid_list))
    print "\nFound RecoveryPoints on Source: {0}".format(SRC_IP)
    for i in out["group_results"][0]["entity_results"]:
      rpt_uuid = i["entity_id"]
      create_time = datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S')
      lau = src_rpt_obj.get(rpt_uuid, get_vm_vg_details=False).loc_agn_uuid
      print "RPT: {0} - LAU: {1} - {2} GMT".format(rpt_uuid, lau, create_time)
      #print "RPT: {0} - LAU: {1} - {2} GMT".format(i["entity_id"], lau, datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S'))
      #print "{0} - {1} GMT".format(i["entity_id"], datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S'))
else:
  print "\nNo RecoveryPoints found on Source: {0}\n".format(SRC_IP)

out = rmt_rpt_obj.get_groups_response(filter_criteria)
rpt_uuid_list = list()
if out["filtered_group_count"] > 0:
  rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
  if get_details:
    print "\nGetting RPT details on Target.\n"
    get_rpt_details(rpt_uuid_list, source=False)
  else:
    #print "\nFound RecoveryPoints on Target:\n{0}".format("\n".join(rpt_uuid_list))
    print "\nFound RecoveryPoints on Target: {0}".format(TGT_IP)
    for i in out["group_results"][0]["entity_results"]:
      rpt_uuid = i["entity_id"]
      create_time = datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S')
      lau = rmt_rpt_obj.get(rpt_uuid, get_vm_vg_details=False).loc_agn_uuid
      print "RPT: {0} - LAU: {1} - {2} GMT".format(rpt_uuid, lau, create_time)
      #print "RPT: {0} - LAU: {1} - {2} GMT".format(i["entity_id"], lau, datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S'))
else:
  print "\nNo RecoveryPoints found on Target: {0}\n".format(TGT_IP)
print "\n"

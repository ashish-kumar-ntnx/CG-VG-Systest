import sys
from framework.vg_entity import VG
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

SRC_IP = SRC_PC_IP
#SRC_IP = TGT_PC_IP
#TGT_IP = TGT_PC_IP

#SRC_IP, TGT_IP = "10.40.216.116", "10.40.216.116"

vg_obj = VG(SRC_IP)
vg_name_uuid_map = vg_obj.get_name_uuid_map()
src_rpt_obj = RecoveryPoint(SRC_IP)
#rmt_rpt_obj = RecoveryPoint(TGT_IP)

vg_name = sys.argv[1]

vg_uuid = vg_name_uuid_map[vg_name]
print "Finding all the recovery_points of the VG: {0} - {1}".format(vg_name, vg_uuid)


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
  "filter_criteria":"disk_group_live_entity_uuid_list=={0}".format(vg_uuid)
}
#print filter_criteria
out = src_rpt_obj.get_groups_response(filter_criteria)
rpt_uuid_list = list()
if out["filtered_group_count"] > 0:
  rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
  print "\nFound RecoveryPoints on Source: {0}".format(SRC_IP)
  for i in out["group_results"][0]["entity_results"]:
    rpt_uuid = i["entity_id"]
    create_time = datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S')
    lau = src_rpt_obj.get(rpt_uuid, get_vm_vg_details=False).loc_agn_uuid
    print "RPT: {0} - LAU: {1} - {2} GMT".format(rpt_uuid, lau, create_time)
else:
  print "\nNo RecoveryPoints found on Source: {0}\n".format(SRC_IP)

"""
out = rmt_rpt_obj.get_groups_response(filter_criteria)
rpt_uuid_list = list()
if out["filtered_group_count"] > 0:
  rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
  print "\nFound RecoveryPoints on Target: {0}".format(TGT_IP)
  for i in out["group_results"][0]["entity_results"]:
    rpt_uuid = i["entity_id"]
    create_time = datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S')
    lau = rmt_rpt_obj.get(rpt_uuid, get_vm_vg_details=False).loc_agn_uuid
    print "RPT: {0} - LAU: {1} - {2} GMT".format(rpt_uuid, lau, create_time)
else:
  print "\nNo RecoveryPoints found on Target: {0}\n".format(TGT_IP)
print "\n"
"""

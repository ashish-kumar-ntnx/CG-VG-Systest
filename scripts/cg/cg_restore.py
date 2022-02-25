import sys
from framework.cg_entity import CG
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = SRC_PC_IP

if len(sys.argv) != 2:
  print "\tUsage: python cg_restore.py <cg-name>\n"
  sys.exit(1)
cg_name = sys.argv[1]

cg_obj = CG(IP)
rpt_obj = RecoveryPoint(IP)

cg = cg_obj.get(cg_name=cg_name)
print "Finding latest recovery_points of the CG: {0} - {1}".format(cg_name, cg.uuid)
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
out = rpt_obj.get_groups_response(filter_criteria)
rpt_uuid_list = list()
if out["filtered_group_count"] > 0:
  rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
latest_rpt_uuid = rpt_uuid_list[0]
print "Latest recovery point is: {0}".format(latest_rpt_uuid)
print "Restoring CG entities(VM/VG) from recovery point: {0}".format(latest_rpt_uuid)
rpt_obj.restore_rec_point(rpt_uuid=latest_rpt_uuid)

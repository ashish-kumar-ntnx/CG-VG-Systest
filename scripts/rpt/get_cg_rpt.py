from framework.cg_entity import CG
from framework.rec_point_entity import RecoveryPoint
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

START = 1
END = 2 #21
cg_obj = CG(SRC_PC_IP)
src_rpt_obj = RecoveryPoint(SRC_PC_IP)
rmt_rpt_obj = RecoveryPoint(TGT_PC_IP)

for i in range(START, END):
  cg_name = "cg-" + str(i)
  print "Finding all the recovery_points of the CG: {0}".format(cg_name)
  cg = cg_obj.get(cg_name=cg_name)
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
  print filter_criteria
  out = src_rpt_obj.get_groups_response(filter_criteria)
  rpt_uuid_list = list()
  if out["filtered_group_count"] > 0:
    rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
    print "\nFound RecoveryPoints on Source:\n{0}".format("\n".join(rpt_uuid_list))
  else:
    print "\nNo RecoveryPoints found on Source.\n"

  out = rmt_rpt_obj.get_groups_response(filter_criteria)
  rpt_uuid_list = list()
  if out["filtered_group_count"] > 0:
    rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
    print "\nFound RecoveryPoints on Target:\n{0}".format("\n".join(rpt_uuid_list))
  else:
    print "\nNo RecoveryPoints found on Target.\n"

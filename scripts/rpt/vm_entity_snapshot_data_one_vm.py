import sys
from framework.mh_vm_entity import VM
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.lib import *

PC_IP = sys.argv[1]
vm_name = sys.argv[2]
clus_uuid = sys.argv[3]


vm_obj = VM(PC_IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
#print vm_name_uuid_map
src_rpt_obj = RecoveryPoint(PC_IP)


print "Finding all the recovery_points of the VM: {0}".format(vm_name)


filter_criteria = {
  "entity_type":"entity_snapshot",
  "group_member_sort_attribute": "_created_timestamp_usecs_",
  "group_member_sort_order": "DESCENDING",
  "filter_criteria":"entity_name=={0};_master_cluster_uuid_=={1}".format(vm_name, clus_uuid)
}
#print filter_criteria
out = src_rpt_obj.get_groups_response(filter_criteria)
if out["filtered_group_count"] > 0:
  entity_snapshot = out["group_results"][0]["entity_results"][0]["entity_id"]
  print "\nVM: {0}, entity_snapshot: {1}".format(vm_name, entity_snapshot)
  #url = "api/nutanix/v3/vm_recovery_points/{0}/restore".format(entity_snapshot)
  #r = send_request("POST", IP, url, json={})
  #out = r.json()

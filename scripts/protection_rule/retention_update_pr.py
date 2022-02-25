import sys
from framework.protection_rule_entity import ProtectionRule
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#IP = TGT_PC_IP
IP = SRC_PC_IP
pr = ProtectionRule(IP)
retention_count = 3

for i in range(1, 11):
  pr_name = "pr-" + str(i)
  pr_obj = pr.get(pr_name=pr_name)
  spec = pr_obj.spec
  spec.pop("status")
  print "Increasing retention_count to {0} for PR: {1}".format(retention_count, pr_name)
  spec["spec"]["resources"]["availability_zone_connectivity_list"][0]["snapshot_schedule_list"][0]["local_snapshot_retention_policy"]["num_snapshots"] = retention_count
  spec["spec"]["resources"]["availability_zone_connectivity_list"][0]["snapshot_schedule_list"][0]["remote_snapshot_retention_policy"]["num_snapshots"] = retention_count
  spec["spec"]["resources"]["availability_zone_connectivity_list"][1]["snapshot_schedule_list"][0]["local_snapshot_retention_policy"]["num_snapshots"] = retention_count
  spec["spec"]["resources"]["availability_zone_connectivity_list"][1]["snapshot_schedule_list"][0]["remote_snapshot_retention_policy"]["num_snapshots"] = retention_count
  pr_obj.update(spec) 

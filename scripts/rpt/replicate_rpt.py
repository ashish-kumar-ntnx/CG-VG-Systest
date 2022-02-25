import sys
from framework.cg_entity import CG
from framework.rec_point_entity import RecoveryPoint
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from datetime import datetime

if len(sys.argv) != 4:
  print "\n\tUsage: python replicate_rpt.py <rpt_uuid> <target_az_ip> <target_cluster_name>\n"
  sys.exit(1)


src_rpt_obj = RecoveryPoint(SRC_PC_IP)
rpt_uuid = sys.argv[1]
target_az_ip = sys.argv[2]
target_cluster_name = sys.argv[3]
print "Replicating RPT: {0} to Target AZ: {1}, Target Cluster: {2}".format(rpt_uuid, target_az_ip, target_cluster_name)
src_rpt_obj.replicate_rec_point(rpt_uuid, target_az_ip, target_cluster_name)

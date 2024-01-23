import sys
from framework.cg_entity import CG
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#INIT_PC = TGT_PC_IP
#TARGET_PC = SRC_PC_IP
#INIT_PES = TGT_CLUS_LIST
#TARGET_PES = SRC_CLUS_LIST
INIT_PC = SRC_PC_IP
TARGET_PC = TGT_PC_IP
INIT_PES = SRC_CLUS_LIST
TARGET_PES = TGT_CLUS_LIST

#SRC_PC_IP = "10.40.216.116"
if len(sys.argv) != 2:
  print "\n\tUsage: python create_cg_rpt_and_replicate.py <cg_name>\n"
  sys.exit(1)

#if len(sys.argv) != 4:
#  print "\n\tUsage: python create_cg_rpt.py <cg_name> <target_az_ip> <target_cluster_name>\n"
#  sys.exit(1)

cg_name = sys.argv[1]
if int(cg_name.split("-")[1]) <= 10:
  target_cluster_name = TARGET_PES[0]
else:
  target_cluster_name = TARGET_PES[1]
#target_az_ip = sys.argv[2]
#target_cluster_name = sys.argv[3]

cg_obj = CG(INIT_PC)
src_rpt_obj = RecoveryPoint(INIT_PC)
#rmt_rpt_obj = RecoveryPoint(Target_PC_IP)

cg = cg_obj.get(cg_name=cg_name)
rpt_uuid = cg.create_recovery_point()
#rpt_uuid = "8cc2ce1b-2ea1-432d-892e-7ad72c5467fb"


#src_rpt_obj = RecoveryPoint(SRC_PC_IP)
print "Replicating RPT: {0} to Target AZ: {1}, Target Cluster: {2}".format(rpt_uuid, TARGET_PC, target_cluster_name)
src_rpt_obj.replicate_rec_point(rpt_uuid, TARGET_PC, target_cluster_name)

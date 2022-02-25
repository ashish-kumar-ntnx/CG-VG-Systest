import sys
from framework.cg_entity import CG
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

#SRC_PC_IP = "10.40.216.116"
if len(sys.argv) != 2:
  print "\n\tUsage: python create_cg_rpt.py <cg_name>\n"
  sys.exit(1)
cg_name = sys.argv[1]

cg_obj = CG(SRC_PC_IP)
src_rpt_obj = RecoveryPoint(SRC_PC_IP)
#rmt_rpt_obj = RecoveryPoint(Target_PC_IP)

cg = cg_obj.get(cg_name=cg_name)
cg.create_recovery_point()

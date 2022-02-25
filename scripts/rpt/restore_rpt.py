import sys
from framework.cg_entity import CG
from framework.rec_point_entity import RecoveryPoint
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from datetime import datetime

IP = SRC_PC_IP

if len(sys.argv) != 2:
  print "\n\tUsage: python restore_rpt.py <rpt_uuid>\n"
  sys.exit(1)

rpt_obj = RecoveryPoint(IP)
rpt_uuid = sys.argv[1]
print "Restoring RPT: {0} on Target AZ: {1}".format(rpt_uuid, IP)
rpt_obj.restore_rec_point(rpt_uuid=rpt_uuid)

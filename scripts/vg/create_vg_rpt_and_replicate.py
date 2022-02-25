import sys
from framework.vg_entity import VG
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
  print "\n\tUsage: python create_vg_rpt_and_replicate.py <vg_name>\n"
  sys.exit(1)

vg_name = sys.argv[1]

vg_obj = VG(INIT_PC)
src_rpt_obj = RecoveryPoint(INIT_PC)
rmt_rpt_obj = RecoveryPoint(TARGET_PC)

vg = vg_obj.get(vg_name=vg_name)
rpt_uuid = vg.create_recovery_point()
#rpt_uuid = "8cc2ce1b-2ea1-432d-892e-7ad72c5467fb"


#src_rpt_obj = RecoveryPoint(SRC_PC_IP)
print "Replicating RPT: {0} to Target AZ: {1}, Target Cluster: {2}".format(rpt_uuid, TARGET_PC, TARGET_PES[0])
src_rpt_obj.replicate_rec_point(rpt_uuid, TARGET_PC, TARGET_PES[0])

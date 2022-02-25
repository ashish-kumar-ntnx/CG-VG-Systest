from framework.rec_point_entity import RecoveryPoint
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from pprint import pprint

SRC_PC_IP = "10.40.216.116"

rp_obj = RecoveryPoint(SRC_PC_IP)
rpt_map = rp_obj.get_all_recovery_points()
pprint(rpt_map)
#rpt = RecoveryPoint.get(uuid="4f2beb92-e7f2-4ab4-9a9e-5a62e9c8cd4c")


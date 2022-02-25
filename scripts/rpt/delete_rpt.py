from framework.rec_point_entity import RecoveryPoint
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

SRC_PC_IP = "10.40.216.116"
rp_obj = RecoveryPoint(SRC_PC_IP)
rpt_obj_map = rp_obj.get_all_recovery_points()
#rpt_obj_map = rp_obj.get_all_recovery_points(return_objects=True)
for rpt_uuid in rpt_obj_map:
  rp_obj.remove(uuid=rpt_uuid)
  #print rpt_obj_map[rpt]["vm_list"]
  #print rpt_obj_map[rpt]["vg_list"]
  #print "\n"

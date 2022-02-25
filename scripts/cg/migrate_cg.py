import sys
from framework.cg_entity import CG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST


cg = CG(SRC_PC_IP)
cg_name = sys.argv[1]

target_az_ip = TGT_PC_IP
if int(cg_name.split("-")[1]) > 10:
  target_cluster_name = TGT_CLUS_LIST[1]
else:
  target_cluster_name = TGT_CLUS_LIST[0]

cg_obj = cg.get(cg_name=cg_name)
print "Triggering CG: {0} - {1} migrate to TGT PC: {2}, TGT CLUSTER: {3}".format(cg_name, cg_obj.uuid, target_az_ip, target_cluster_name)
cg_obj.migrate(target_az_ip, target_cluster_name)

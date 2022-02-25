import sys
from framework.cg_entity import CG
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
SRC_PC_IP = "10.40.216.116"
cg = CG(SRC_PC_IP)

cg_name = sys.argv[1]
target_az_id = "1412e47b-590d-4481-915a-9a6cb00d466c"
target_cluster_id = "0005c4c8-5f34-9e2c-0000-0000000282df"


cg_obj = cg.get(cg_name=cg_name)
cg_obj.migrate(target_az_id, target_cluster_id)

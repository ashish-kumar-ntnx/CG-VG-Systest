import sys
from framework.cg_entity import CG
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
SRC_PC_IP = "10.40.216.116"
cg = CG(SRC_PC_IP)

cg_name = sys.argv[1]

cg_obj = cg.get(cg_name=cg_name)
cg_obj.remove()

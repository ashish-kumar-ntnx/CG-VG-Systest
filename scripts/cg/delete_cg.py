from framework.cg_entity import CG
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST

IP = TGT_PC_IP
IP = SRC_PC_IP

cg = CG(IP)

for i in range(1, 11):
  cg_name = "cg-" + str(i)
  cg_obj = cg.get(cg_name=cg_name)
  if cg_obj:
    cg_obj.remove()

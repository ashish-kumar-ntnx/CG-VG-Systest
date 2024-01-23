from framework.rec_point_entity import RecoveryPoint
#from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
import time
import threading
import sys

PC_IP = sys.argv[1]
rp_obj = RecoveryPoint(PC_IP)
for _ in range(1, 101):
  #cluster_uuid = "0005fc81-ff57-3b9d-7e83-0cc47a9b0a8c"
  cluster_uuid = None
  rpt_map = rp_obj.get_all_recovery_points(cluster_uuid=cluster_uuid)
  rpt_uuid_list = rpt_map.keys()
  delete_chuck = 15

  for i in range(1, len(rpt_uuid_list), delete_chuck):
    threads = list()
    for j in range(delete_chuck):
      try:
        x = threading.Thread(target=rp_obj.remove, args=(rpt_uuid_list[i+j],))
        threads.append(x)
      except:
        pass
    for th in threads:
      th.start()
    for th in threads:
      th.join()




#for rpt_uuid in rpt_map:
#  rp_obj.remove(uuid=rpt_uuid)

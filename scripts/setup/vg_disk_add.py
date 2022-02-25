import time
from pprint import pprint
import sys
from framework.lib import *
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.cluster_entity import Cluster
from framework.ctr_entity import Ctr
from framework.vm_entity import VM
from framework.vg_entity import VG
from framework.subnet_entity import Subnet
from setup_config import *

IP = SRC_PC_IP
CLUS_LIST = SRC_CLUS_LIST

#IP = TGT_PC_IP
#CLUS_LIST = TGT_CLUS_LIST

clus_obj = Cluster(IP)
ctr_obj = Ctr(IP)
vg_obj = VG(IP)
vg_name_uuid_map = vg_obj.get_name_uuid_map()
#print vg_name_uuid_map.keys()
#print len(vg_name_uuid_map)
#vg_name_uuid_map = vg_obj.get_name_uuid_map(cluster_uuid="0005c91e-935e-3827-0000-0000000109fe")
#print len(vg_name_uuid_map)
#print " ".join(vg_name_uuid_map.keys())

for clus_name in CLUS_LIST:
  ctr_name_uuid_map = ctr_obj.get_name_uuid_map(cluster_name=clus_name)
  clus = clus_obj.get(cluster_name=clus_name)
  cluster_uuid = clus.uuid
  #cluster_uuid = "0005c91e-935e-3827-0000-0000000109fe"

  if clus_name in ["PC-A-PE-1", "PC-B-PE-1"]:
    vg_prefix = "vg-a-"
  elif clus_name in ["PC-A-PE-2", "PC-B-PE-2"]:
    vg_prefix = "vg-b-"

  #start, end = 51, 60
  start, end = 1, 101
  for i in range(start, end):
    vg_name_list = [vg_prefix + str(i), vg_prefix + str(i + 100)]
    for vg_name in vg_name_list:
      #if vg_name not in ["vg-a-19", "vg-a-60"]:
      #  continue
      vg_uuid = vg_name_uuid_map[vg_name]
      vg = vg_obj.get(vg_uuid=vg_uuid)
      print "checking VG: {0} - {1}".format(vg_name, vg_uuid)
      #print vg.disk_list
      if len(vg.disk_list) != 10:
        vg_spec = get_vg_spec(vg_name, clus_name, cluster_uuid, ctr_name_uuid_map)
        spec = vg_spec["spec"]
        disk_list = vg_spec["disk_list"]
        print "Adding disks to the {0} - {1}".format(vg_name, vg_uuid)
        for disk_spec in disk_list:
          vg.add_disk(disk_spec=disk_spec)


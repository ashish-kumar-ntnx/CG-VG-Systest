import sys
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST, SETUP_TYPE
if SETUP_TYPE == "ESX":
  from framework.mh_vm_entity import VM
elif SETUP_TYPE == "AHV":
  from framework.vm_entity import VM
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.lib import *

IP = SRC_PC_IP
#IP = TGT_PC_IP

#SRC_IP, TGT_IP = "10.40.216.116", "10.40.216.116"

vm_obj = VM(IP)
vm_name_uuid_map = vm_obj.get_name_uuid_map()
#print vm_name_uuid_map
src_rpt_obj = RecoveryPoint(IP)
#rmt_rpt_obj = RecoveryPoint(TGT_IP)

START, END = 1, 161
vm_prefix = "vm-"
clus_uuid = "00060bda-1f67-8b6b-0000-0000000158bd"
#clus_uuid = "0005f6d9-3100-c161-0000-000000011f39"

for i in range(START, END):
  suf = str(i).rjust(4, '0')
  vm_name = "ST_PC-A-PE-1_vdb-vdi_dp-cmp-dl_centos7_scsi_" + suf
  if vm_name in vm_name_uuid_map:
    continue
  #vm_name = vm_prefix + str(i)
  print "Finding all the recovery_points of the VM: {0}".format(vm_name)


  filter_criteria = {
    "entity_type":"entity_snapshot",
    "group_member_sort_attribute": "_created_timestamp_usecs_",
    "group_member_sort_order": "DESCENDING",
    "filter_criteria":"entity_name=={0};_master_cluster_uuid_=={1}".format(vm_name, clus_uuid)
  }
  #print filter_criteria
  out = src_rpt_obj.get_groups_response(filter_criteria)
  #print out
  if out["filtered_group_count"] > 0:
    entity_snapshot = out["group_results"][0]["entity_results"][0]["entity_id"]
    print "\nVM: {0}, entity_snapshot: {1}".format(vm_name, entity_snapshot)
    url = "api/nutanix/v3/vm_recovery_points/{0}/restore".format(entity_snapshot)
    r = send_request("POST", IP, url, json={})
    out = r.json()
"""
  out = rmt_rpt_obj.get_groups_response(filter_criteria)
  rpt_uuid_list = list()
  if out["filtered_group_count"] > 0:
    rpt_uuid_list = [i["entity_id"] for i in out["group_results"][0]["entity_results"]]
    print "\nFound RecoveryPoints on Target: {0}".format(TGT_IP)
    for i in out["group_results"][0]["entity_results"]:
      rpt_uuid = i["entity_id"]
      create_time = datetime.utcfromtimestamp(int(i["data"][0]["values"][0]["values"][0])/1000000).strftime('%Y-%m-%d %H:%M:%S')
      lau = rmt_rpt_obj.get(rpt_uuid, get_vm_vg_details=False).loc_agn_uuid
      print "RPT: {0} - LAU: {1} - {2} GMT".format(rpt_uuid, lau, create_time)
  else:
    print "\nNo RecoveryPoints found on Target: {0}\n".format(TGT_IP)
  print "\n"
"""

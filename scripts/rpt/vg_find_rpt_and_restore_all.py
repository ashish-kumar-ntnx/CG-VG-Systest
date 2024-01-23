import sys
from framework.vg_entity import VG
from framework.lib import *
from framework.rec_point_entity import RecoveryPoint
from datetime import datetime
from framework.config import SRC_PC_IP, SRC_CLUS_LIST, TGT_PC_IP, TGT_CLUS_LIST
from framework.const import get_ntnx_req_id

IP = SRC_PC_IP
vg_obj = VG(IP)

vg_name_uuid_map = vg_obj.get_name_uuid_map()

source_cluster_uuid = "00060bda-1f67-8b6b-0000-0000000158bd"

for i in range(1, 161):
  vg_name_list = ["vdi-vm-{0}-vg-1".format(i)]
  if i > 80:
    vg_name_list.append("vdi-vm-{0}-vg-2".format(i))
  for vg_name in vg_name_list:
    if vg_name in vg_name_uuid_map:
      continue
    print "Finding VG RPT of VG: {0}".format(vg_name)

    spec = {"entity_type":"volume_group_recovery_point","group_member_sort_attribute":"creation_time_usecs","group_member_sort_order":"ASCENDING","group_member_attributes":[{"attribute": "top_level_recovery_point_uuid"}, {"attribute":"source_cluster_uuid"},{"attribute":"creation_time_usecs"}],"filter_criteria":"source_cluster_uuid=={0};volume_group_name==.*{1}.*".format(source_cluster_uuid ,vg_name)}

    #print spec

    url = "api/nutanix/v3/groups"

    r = send_request("POST", IP, url, json=spec)
    out = r.json()

    if out["filtered_entity_count"] == 0:
      print "No recovery point found for VG: {0} on cluster: {1}".format(vg_name, source_cluster_uuid)
    else:
      rpt_uuid = out["group_results"][0]["entity_results"][0]["data"][0]["values"][0]["values"][0]
      url = "api/dataprotection/v4.0.a5/config/recovery-points/{0}/volume-group-recovery-points".format(rpt_uuid)
      #print rpt_uuid, url
      r = send_request("GET", IP, url)
      out = r.json()
      vg_rpt_uuid = out["data"][0]["volumeGroupRecoveryPointExtId"]
      #vg_rpt_uuid = out["data"][0]["extId"]
      print "For VG: {0} on cluster: {1} vg_rpt: {2}, top_level_rpt: {3}".format(vg_name, source_cluster_uuid, vg_rpt_uuid, rpt_uuid)

    url = "api/dataprotection/v4.0.a5/config/recovery-points/{0}/$actions/restore".format(rpt_uuid, vg_rpt_uuid)
    vg_restore_spec = {"clusterExtId": source_cluster_uuid,"volumeGroupRecoveryPointRestoreOverrides":[{"volumeGroupRecoveryPointExtId":vg_rpt_uuid,"volumeGroupOverrideSpec":{"name":vg_name}}]}
    #url = "api/dataprotection/v4.0.a3/config/recovery-points/{0}/volume-group-recovery-points/{1}/$actions/restore".format(rpt_uuid, vg_rpt_uuid)
    #url = "api/dataprotection/v4.0.a2/config/recovery-points/{0}/$actions/restore".format(rpt_uuid)

    print "Restoring VG: {0}".format(vg_name)
    ntnx_req_id = get_ntnx_req_id()
    r = send_request("POST", IP, url, json=vg_restore_spec, ntnx_req_id=ntnx_req_id)
    #r = send_request("POST", IP, url, json={"name": vg_name})
    print r.status_code

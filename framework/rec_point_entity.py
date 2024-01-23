from framework.lib import *
from framework.const import get_ntnx_req_id
from framework.cluster_entity import Cluster
import time

DEBUG=False

class VmRecoveryPoint(object):
  def __init__(self, rpt_uuid):
    self.rpt_uuid = rpt_uuid
    self.uuid = None
    self.name = None
    self.vm_name = None
    self.vm_uuid = None
    self.cg_uuid = None
    self.creation_time = None
    self.expiry_time = None
    self.status = None
    self.rp_type = None
    self.loc_agn_uuid = None

class VmDiskRecoveryPoint(object):
  def __init__(self, rpt_uuid, vm_rpt_uuid):
    self.rpt_uuid = rpt_uuid
    self.vm_rpt_uuid = vm_rpt_uuid
    self.uuid = None
    self.name = None
    self.disk_uuid = None
    self.disk_capacity = None
    self.creation_time = None
    self.expiry_time = None
    self.status = None
    self.rp_type = None
    self.loc_agn_uuid = None

class VgRecoveryPoint(object):
  def __init__(self, rpt_uuid):
    self.rpt_uuid = rpt_uuid
    self.uuid = None
    self.name = None
    self.vg_name = None
    self.vg_uuid = None
    self.cg_uuid = None
    self.creation_time = None
    self.expiry_time = None
    self.status = None
    self.rp_type = None
    self.loc_agn_uuid = None

class VgDiskRecoveryPoint(object):
  def __init__(self, rpt_uuid, vg_rpt_uuid):
    self.rpt_uuid = rpt_uuid
    self.vg_rpt_uuid = vg_rpt_uuid
    self.uuid = None
    self.name = None
    self.disk_uuid = None
    self.disk_capacity = None
    self.creation_time = None
    self.expiry_time = None
    self.status = None
    self.rp_type = None
    self.loc_agn_uuid = None

class RecoveryPoint(object):
  def __init__(self, pc_ip, name=None, uuid=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.name = name
    self.creation_time = None
    self.expiry_time = None
    self.status = None
    self.rp_type = None
    self.loc_agn_uuid = None

  def get(self, uuid, get_vm_vg_details=True):
    if get_vm_vg_details:
      print "Creating RecoveryPoint object for: {0}".format(uuid)
    url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}".format(uuid)
    r = send_request("GET", self.pc_ip, url, debug=DEBUG)
    out = r.json()
    #print out
    data = out["data"]
    if "name" in data.keys():
      name = data["name"]
    else:
      name = None
    rpt = RecoveryPoint(self.pc_ip, name=name, uuid=uuid)
    rpt.uuid = data["extId"]
    rpt.creation_time = data["creationTime"]
    rpt.expiry_time = data["expirationTime"]
    rpt.status = data["status"]
    rpt.rp_type = data["recoveryPointType"]
    rpt.loc_agn_uuid = data["locationAgnosticId"]
    if get_vm_vg_details:
      rpt.vm_rpt_list = self.get_vm_rpt_list(rpt.uuid)
      rpt.vg_rpt_list = self.get_vg_rpt_list(rpt.uuid)
    return rpt

  def get_vm_rpt_list(self, rpt_uuid):
    vm_rpt_list = list()
    url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}/vm-recovery-points".format(rpt_uuid)
    r = send_request("GET", self.pc_ip, url, debug=DEBUG)
    out = r.json()
    if out["$dataItemDiscriminator"] == "EMPTY_LIST":

      return vm_rpt_list

    for i in out["data"]:
      v = VmRecoveryPoint(rpt_uuid)
      v.uuid = i["extId"]
      v.name = i["name"]
      v.vm_name = i["vm"]["name"]
      v.vm_uuid = i["vm"]["vmExtId"]
      v.cg_uuid = i["consistencyGroupExtId"]
      v.creation_time = i["creationTime"]
      v.expiry_time = i["expirationTime"]
      v.status = i["status"]
      v.rp_type = i["recoveryPointType"]
      v.loc_agn_uuid = i["locationAgnosticId"]
      v.vm_disk_rpt_list = self.get_vm_disk_rpt_list(rpt_uuid, v.uuid)
      vm_rpt_list.append(v)

    return vm_rpt_list
      

  def get_vm_disk_rpt_list(self, rpt_uuid, vm_rpt_uuid):
    vm_disk_rpt_list = list()
    url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}/vm-recovery-points/{1}/disk-recovery-points".format(rpt_uuid, vm_rpt_uuid)
    r = send_request("GET", self.pc_ip, url, debug=DEBUG)
    out = r.json()
    if out["$dataItemDiscriminator"] == "EMPTY_LIST":
      return vm_disk_rpt_list

    for i in out["data"]:
      v = VmDiskRecoveryPoint(rpt_uuid, vm_rpt_uuid)
      v.uuid = i["extId"]
      v.name = i["name"]
      v.disk_uuid = i["disk"]["diskExtId"]
      v.disk_capacity = i["disk"]["capacityBytes"]
      v.creation_time = i["creationTime"]
      v.expiry_time = i["expirationTime"]
      v.status = i["status"]
      v.rp_type = i["recoveryPointType"]
      v.loc_agn_uuid = i["locationAgnosticId"]
      vm_disk_rpt_list.append(v)

    return vm_disk_rpt_list

  def get_vg_rpt_list(self, rpt_uuid):
    vg_rpt_list = list()
    url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}/volume-group-recovery-points".format(rpt_uuid)
    r = send_request("GET", self.pc_ip, url, debug=DEBUG)
    out = r.json()
    if out["$dataItemDiscriminator"] == "EMPTY_LIST":
      return vg_rpt_list

    for i in out["data"]:
      v = VgRecoveryPoint(rpt_uuid)
      v.uuid = i["extId"]
      v.name = i["name"]
      v.vg_name = i["volumeGroup"]["name"]
      v.vg_uuid = i["volumeGroup"]["volumeGroupExtId"]
      v.cg_uuid = i["consistencyGroupExtId"]
      v.creation_time = i["creationTime"]
      v.expiry_time = i["expirationTime"]
      v.status = i["status"]
      v.rp_type = i["recoveryPointType"]
      v.loc_agn_uuid = i["locationAgnosticId"]
      v.vg_disk_rpt_list = self.get_vg_disk_rpt_list(rpt_uuid, v.uuid)
      vg_rpt_list.append(v)

    return vg_rpt_list
      
  def get_vg_disk_rpt_list(self, rpt_uuid, vg_rpt_uuid):
    vg_disk_rpt_list = list()
    url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}/volume-group-recovery-points/{1}/disk-recovery-points".format(rpt_uuid, vg_rpt_uuid)
    r = send_request("GET", self.pc_ip, url, debug=DEBUG)
    out = r.json()
    if out["$dataItemDiscriminator"] == "EMPTY_LIST":
      return vg_disk_rpt_list

    for i in out["data"]:
      v = VgDiskRecoveryPoint(rpt_uuid, vg_rpt_uuid)
      v.uuid = i["extId"]
      v.name = i["name"]
      v.disk_uuid = i["disk"]["diskExtId"]
      v.disk_capacity = i["disk"]["capacityBytes"]
      v.creation_time = i["creationTime"]
      v.expiry_time = i["expirationTime"]
      v.status = i["status"]
      v.rp_type = i["recoveryPointType"]
      v.loc_agn_uuid = i["locationAgnosticId"]
      vg_disk_rpt_list.append(v)

    return vg_disk_rpt_list

  def list_all(self):
    pass

  def get_all_recovery_points(self, return_objects=False, cluster_uuid=None):
    url = "api/nutanix/v3/groups"
    payload = {"entity_type":"recovery_point","group_member_attributes":[{"attribute":"vm_live_entity_uuid_list"},{"attribute":"disk_group_live_entity_uuid_list"}]}
    if cluster_uuid:
      payload["filter_criteria"] = "_master_cluster_uuid_=={0}".format(cluster_uuid)
    r = send_request("POST", self.pc_ip, url, json=payload)
    out = r.json()
    total_rpt = out["filtered_entity_count"]
    rpt_map = dict()
    for i in out["group_results"][0]["entity_results"]:
      rpt_uuid = i["entity_id"]
      vm_list, vg_list = [], []
      try:
        vm_list = i["data"][0]["values"][0]["values"]
      except:
        pass
      try:
        vg_list = i["data"][1]["values"][0]["values"]
      except:
        pass

      rpt_map[rpt_uuid] = {"vm_list": vm_list, "vg_list": vg_list}

    if not return_objects:
      return rpt_map
    
    rpt_obj_map = dict()
    t1 = time.time()
    for rpt_uuid in rpt_map:
      print "\nRemaning RPTs for object creation: {0}\n".format(total_rpt)
      total_rpt -= 1
      r = self.get(uuid=rpt_uuid)
      t2 = time.time()
      print "Time taken for object creation: {0} seconds".format(int(t2-t1))
      t1 = t2
      r.live_vm_list = rpt_map[rpt_uuid]["vm_list"]
      r.live_vg_list = rpt_map[rpt_uuid]["vg_list"]
      rpt_obj_map[rpt_uuid] = r
    return rpt_obj_map

  def get_groups_response(self, payload):
    url = "api/nutanix/v3/groups"
    r = send_request("POST", self.pc_ip, url, json=payload)
    return r.json()

  def create(self):
    pass

  def remove(self, uuid=None):
    if not uuid:
      uuid = self.uuid
    print "Deleting Recovery Point: {0}".format(uuid)
    #url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}".format(uuid)
    url = "api/dataprotection/v4.0.a5/config/recovery-points/{0}".format(uuid)
    ntnx_req_id = get_ntnx_req_id()
    r = send_request("DELETE", self.pc_ip, url, ntnx_req_id=ntnx_req_id)
    print r.status_code

  def restore_rec_point(self, rpt_uuid=None):
    if not rpt_uuid:
      rpt_uuid=self.uuid
    url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}/$actions/restore".format(rpt_uuid)
    r = send_request("POST", self.pc_ip, url)
    print r.status_code
    if r.status_code == 202:
      out = r.json()
      print "Recovery Point restore triggerd successfully\nTask URL: {0}\n".format(out["metadata"]["links"][0]["href"])
    else:
      print "Recovery Point restore failed to get triggered, error: {0}\n".format(r.text)

  def replicate_rec_point(self, rpt_uuid, target_az_ip, target_cluster_name):
    
    Clus = Cluster(target_az_ip)
    clus_obj = Clus.get(cluster_name=target_cluster_name)

    # GET TARGET AZ UUID
    url = "api/nutanix/v3/availability_zones/list"
    payload = {"filter": "name==Local AZ"}
    r = send_request("POST", target_az_ip, url, json=payload)
    out = r.json()
    az_mgmt_url = out["entities"][0]["spec"]["resources"]["management_url"]

    payload = {"filter": "name!=Local AZ"}
    r = send_request("POST", self.pc_ip, url, json=payload)
    out = r.json()
    target_az_id = ""
    for i in out["entities"]:
      if i["spec"]["resources"]["management_url"] == az_mgmt_url:
        target_az_id = i["metadata"]["uuid"]
        break
    
    url = "api/dataprotection/v4.0.a1/config/recovery-points/{0}/$actions/replicate".format(rpt_uuid)
    #payload = {"targetAvailabilityZoneId": target_az_id, "targetClusterId": clus_obj.uuid} 
    payload = {"targetAvailabilityZoneId": "6380792c-820f-4151-90b4-48acb6cf2a81", "targetClusterId": clus_obj.uuid} 
    #payload = {"targetAvailabilityZoneId": "d942ac21-18e9-42af-8cc8-b609dfc65c5f", "targetClusterId": clus_obj.uuid} 
    r = send_request("POST", self.pc_ip, url, json=payload)
    if r.status_code == 202:
      out = r.json()
      print "Recovery Point replication triggerd successfully\nTask URL: {0}\n".format(out["metadata"]["links"][0]["href"])
    else:
      print "Recovery Point replication failed to get triggered, error: {0}\n".format(r.text)

  # VM ops
  def list_all_vm_rec_points(self):
    pass

  def get_vm_rec_point(self):
    pass

  def restore_vm_rec_point(self):
    pass

  def list_all_vm_disk_rec_point(self):
    pass

  def get_vm_disk_rec_point(self):
    pass

  # VG ops
  def list_all_vg_rec_points(self):
    pass

  def get_vg_rec_point(self):
    pass

  def restore_vg_rec_point(self):
    pass

  def list_all_vg_disk_rec_point(self):
    pass

  def get_vg_disk_rec_point(self):
    pass

from lib import *
from framework.cluster_entity import Cluster
import datetime
from const import CG_API_VERSION

class CG(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.name = name
    self.spec = spec
    self.vm_list = None
    self.vg_list = None

  def create(self, cg_name, vm_list, vg_list):
    cg_spec = dict()
    cg_spec["name"] = cg_name
    cg_spec["members"] = list()

    for vm in vm_list:
      tmp = dict()
      tmp["entityType"] = "VM"
      tmp["extId"] = vm
      cg_spec["members"].append(tmp)

    for vg in vg_list:
      tmp = dict()
      tmp["entityType"] = "VOLUME_GROUP"
      tmp["extId"] = vg
      cg_spec["members"].append(tmp)

    print "Creating CG: {0} ...".format(cg_name)
    print cg_spec
    url = "api/dataprotection/{0}/config/consistency-groups".format(CG_API_VERSION)
    r = send_request("POST", self.pc_ip, url, json=cg_spec)
    out = r.json()
    print out
    cg_uuid = out["data"]["extId"]
    obj = CG(self.pc_ip, uuid=cg_uuid, name=cg_name)
    obj.vm_list = vm_list
    obj.vg_list = vg_list
    return obj

  def remove(self):
    print "Deleting CG: {0} !!!".format(self.name)
    url = "api/dataprotection/{0}/config/consistency-groups/{1}".format(CG_API_VERSION, self.uuid)
    r = send_request("DELETE", self.pc_ip, url)
    print "Delete API status_code: {0}\n".format(r.status_code)

  def list_all(self):
    url = "api/dataprotection/{0}/config/consistency-groups".format(CG_API_VERSION)
    r = send_request("GET", self.pc_ip, url)
    out = r.json()
    return out

  def get(self, cg_name=None, cg_uuid=None):
    if cg_uuid:
      url = "api/dataprotection/{0}/config/consistency-groups/{1}".format(CG_API_VERSION, cg_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()["data"]
    else:
      out = self.list_all()
      if out["$dataItemDiscriminator"] == "EMPTY_LIST":
        print "There are no CG on this PC."
        return None
      for i in out["data"]:
        if i["name"] == cg_name:
          spec = i
          cg_uuid = i["extId"]
          break
      else:
        print "CG not found"
        return
    c = CG(self.pc_ip, uuid=cg_uuid, spec=spec, name=spec["name"])
    vm_list, vg_list = [], []
    for i in spec["members"]:
      if i["entityType"] == "VM":
        vm_list.append(i["extId"])
      if i["entityType"] == "VOLUME_GROUP":
        vg_list.append(i["extId"])
    c.vm_list = vm_list
    c.vg_list = vg_list
    return c

  def get_json(self):
    url = "api/dataprotection/{0}/config/consistency-groups/{1}".format(CG_API_VERSION, self.uuid)
    r = send_request("GET", self.pc_ip, url)
    return r.json()["data"]

  def update(self):
    pass

  def migrate(self, target_az_ip, target_cluster_name):
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

    url = "api/dataprotection/{0}/config/consistency-groups/{1}/$actions/migrate".format(CG_API_VERSION, self.uuid)
    payload = {"targetAvailabilityZoneId": target_az_id, "targetClusterId": clus_obj.uuid}
    r = send_request("POST", self.pc_ip, url, json=payload)
    print r.status_code
    if r.status_code == 202:
      out = r.json()
      print "CG: {0} - {1} migrate triggerd successfully\nTask URL: {2}\n".format(self.name, self.uuid, out["metadata"]["links"][0]["href"])
    else:
      print "CG: {0} - {1} migrate failed to get triggered, error: {2}\n".format(self.name, self.uuid, r.text)

  def migrate_1(self, target_az_id, target_cluster_id):
    url = "api/dataprotection/{0}/config/consistency-groups/{1}/$actions/migrate".format(CG_API_VERSION, self.uuid)
    payload = {"targetAvailabilityZoneId": target_az_id, "targetClusterId": target_cluster_id}
    r = send_request("POST", self.pc_ip, url, json=payload)
    print r.status_code
    if r.status_code == 202:
      out = r.json()
      print "CG: {0} - {1} migrate triggerd successfully\nTask URL: {2}\n".format(self.name, self.uuid, out["metadata"]["links"][0]["href"])
    else:
      print "CG: {0} - {1} migrate failed to get triggered, error: {2}\n".format(self.name, self.uuid, r.text)

  def create_recovery_point(self, rpt_name=None, rpt_type="CRASH_CONSISTENT"):
    if not rpt_name:
      rpt_name = "{0}-rec-point-{1}".format(self.name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    payload = {"name": rpt_name, "recoveryPointType": rpt_type}
    print "Creating RecoveryPoint of CG: {0} - {1} with RecoveryPoint Name: {2}".format(self.name, self.uuid, rpt_name)
    url = "api/dataprotection/{0}/config/consistency-groups/{1}/$actions/create-recovery-point".format(CG_API_VERSION, self.uuid)
    r = send_request("POST", self.pc_ip, url, json=payload)
    if r.status_code == 201:
      out = r.json()
      print "Recovery Point created successfully, extID: {0}\n".format(out["data"]["extId"])
      return out["data"]["extId"]
    else:
      print "Recovery Point creation failed, with error: {0}\n".format(r.text)
      return None

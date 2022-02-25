from lib import *

class Ctr(object):
  def __init__(self, pc_ip, uuid=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.name = name
    self.cluster_name = None
    self.cluster_uuid = None

  def create(self):
    pass

  def remove(self):
    pass

  def list_all(self, cluster_name=None):
    ctr_list = list()
    url = "api/nutanix/v3/groups"
    body = {"entity_type":"storage_container","group_member_attributes":[{"attribute":"container_name"},{"attribute":"cluster_name"},{"attribute":"cluster"}]}
    if cluster_name:
      body["filter_criteria"] = "cluster_name=={0}".format(cluster_name)
    r = send_request("POST", self.pc_ip, url, json=body)
    out = r.json()
    for i in out["group_results"][0]["entity_results"]:
      tmp = dict()
      tmp["name"] = i["data"][0]["values"][0]["values"][0]
      tmp["cluster_name"] = i["data"][1]["values"][0]["values"][0]
      tmp["cluster_uuid"] = i["data"][2]["values"][0]["values"][0]
      tmp["uuid"] = i["entity_id"]    
      ctr_list.append(tmp)
    return ctr_list

  def get_name_uuid_map(self, cluster_name=None):
    ctr_name_uuid_map = dict()
    out = self.list_all(cluster_name=cluster_name)
    for i in out:
      ctr_name_uuid_map[i["name"]] = i["uuid"]
    return ctr_name_uuid_map

  def get(self, ctr_name, cluster_name):
    ctr_list = self.list_all()
    for ctr in ctr_list:
      if ctr["name"] == ctr_name and ctr["cluster_name"] == cluster_name:
        c = Ctr(self.pc_ip, uuid=ctr["uuid"], name=ctr["name"])
        c.cluster_name = ctr["cluster_name"]
        c.cluster_uuid = ctr["cluster_uuid"]
        return c
    print "Ctr not found."
    return

  def get_cluster(self):
    pass

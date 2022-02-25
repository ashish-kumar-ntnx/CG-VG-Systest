from lib import *

class Subnet(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.spec = spec
    self.name = name
    self.cluster_name = None
    self.cluster_uuid = None

  def create(self, vlan_name, vlan_id, cluster_uuid, cluster_name, vswitch="br0", subnet_type="VLAN"):
    spec = dict()
    spec["name"] = vlan_name
    spec["cluster_reference"] = dict()
    spec["cluster_reference"]["kind"] = "cluster"
    spec["cluster_reference"]["name"] = cluster_name
    spec["cluster_reference"]["uuid"] = cluster_uuid
    spec["resources"] = dict()
    spec["resources"]["vswitch_name"] = vswitch
    spec["resources"]["subnet_type"] = subnet_type
    spec["resources"]["vlan_id"] = vlan_id

    url = "api/nutanix/v3/subnets"
    r = send_request("POST", self.pc_ip, url, json=spec)
    out = r.json()
    time.sleep(5)
    #task_uuid = out["status"]["execution_context"]["task_uuid"]
    self.uuid = uuid
    self.name = vlan_name
    return self

  def remove(self):
    pass

  def list_all(self):
    url = "api/nutanix/v3/subnets/list"
    r = send_request("POST", self.pc_ip, url, json={})
    out = r.json()
    return out

  def get(self, vlan_uuid=None, vlan_name=None, cluster_name=None):
    if vlan_uuid:
      url = "api/nutanix/v3/subnets/{0}".format(vlan_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()
    else:
      out = self.list_all()
      for i in out["entities"]:
        if i["spec"]["name"] == vlan_name and i["spec"]["cluster_reference"]["name"] == cluster_name:
          spec = i
          vlan_uuid = i["metadata"]["uuid"]
          break
      else:
        print "VLAN not found"
        return
    s = Subnet(self.pc_ip, uuid=vlan_uuid, spec=spec, name=spec["spec"]["name"])
    s.cluster_name = spec["spec"]["cluster_reference"]["name"]
    s.cluster_uuid = spec["spec"]["cluster_reference"]["uuid"]
    return s

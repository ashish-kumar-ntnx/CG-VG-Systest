from lib import *

class Cluster(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.spec = spec
    self.name = name
    self.is_pc = False

  def list_all(self):
    url = "api/nutanix/v3/clusters/list"
    r = send_request("POST", self.pc_ip, url, json={})
    out = r.json()
    return out

  def get(self, cluster_uuid=None, cluster_name=None):
    if cluster_uuid:
      url = "api/nutanix/v3/clusters/{0}".format(cluster_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()
    else:
      out = self.list_all()
      #print out
      for i in out["entities"]:
        if i["spec"]["name"] == cluster_name:
          spec = i
          cluster_uuid = i["metadata"]["uuid"]
          break
      else:
        print "Cluster not found"
        return
    s = Cluster(self.pc_ip, uuid=cluster_uuid, spec=spec, name=spec["spec"]["name"])
    try:
      if spec["status"]["resources"]["config"]["service_list"][0] == "PRISM_CENTRAL":
        self.is_pc = True
    except:
      pass
    return s
  
  def get_dsip(self):
    return self.spec["status"]["resources"]["network"]["external_data_services_ip"]

  def get_v1_ip(self):
    return self.spec["status"]["resources"]["network"]["external_ip"]

  def get_json(self):
    url = "api/nutanix/v3/clusters/{0}".format(self.uuid)
    r = send_request("GET", self.pc_ip, url)
    return r.json()

  def list_vms(self):
    pass

  def list_cgs(self):
    pass

  def list_vgs(self):
    pass

  def list_images(self):
    pass

  def list_categories(self):
    pass

  def list_subnets(self):
    pass


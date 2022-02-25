from lib import *

class Image(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.spec = spec
    self.name = name
    self.cluster_uuid_list = None

  def create(self):
    pass

  def remove(self):
    pass

  def list_all(self):
    url = "api/nutanix/v3/images/list"
    r = send_request("POST", self.pc_ip, url, json={})
    out = r.json()
    return out

  def get(self, image_uuid=None, image_name=None):
    if image_uuid:
      url = "api/nutanix/v3/images/{0}".format(image_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()
    else:
      out = self.list_all()
      for i in out["entities"]:
        if i["spec"]["name"] == image_name:
          spec = i
          image_uuid = i["metadata"]["uuid"]
          break
      else:
        print "Image not found"
        return
    s = Image(self.pc_ip, uuid=image_uuid, spec=spec, name=spec["spec"]["name"])
    s.cluster_uuid_list = [i["uuid"] for i in spec["status"]["resources"]["current_cluster_reference_list"]]
    return s

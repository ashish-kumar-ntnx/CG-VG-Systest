from lib import *
from cluster_entity import Cluster
from category_entity import Category
import datetime
from const import VG_API_VERSION, VG_ETAG_REQUIRED

class VG(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.spec = spec
    self.name = name
    self.iscsi_target = None
    self.cluster = None
    self.category_list = None
    self.disk_list = None
    self.iscsi_attachment_list = None
    self.hyp_attachment_list = None

  def create(self, vg_name=None, cluster_name=None, vg_spec=None):
    if not vg_spec: 
      clus = Cluster(self.pc_ip)
      c = clus.get(cluster_name=cluster_name)
      cluster_id = c.uuid
      vg_spec = dict()
      vg_spec["name"] = vg_name
      vg_spec["description"] = "VG: {0} on Cluster: {1}".format(vg_name, cluster_name)
      vg_spec["sharingStatus"] = "SHARED"
      vg_spec["iscsiTargetPrefix"] = vg_name
      vg_spec["clusterReference"] = cluster_id
      print "Creating VG: {0} ...".format(vg_name)

    #url = "api/storage/v4.0.a1/config/volume-groups"
    url = "api/storage/{0}/config/volume-groups".format(VG_API_VERSION)
    print vg_spec
    r = send_request("POST", self.pc_ip, url, json=vg_spec)
    out = r.json()
    print out
    task_url = out["metadata"]["links"][0]["href"]
    print "TASK URL: {0}".format(task_url)
    return task_url

  def remove(self):
    url = "api/storage/{0}/config/volume-groups/{1}".format(VG_API_VERSION, self.uuid)
    r = send_request("DELETE", self.pc_ip, url)
    print r.status_code
    out = r.json()
    return out["data"]["extId"]

  def list_all(self):
    url = "api/storage/{0}/config/volume-groups".format(VG_API_VERSION)
    r = send_request("GET", self.pc_ip, url)
    out = r.json()
    total_count = out["metadata"]["totalAvailableResults"]
    limit = 50
    out = None
    for i in range(0, (total_count/limit) + 1):
      limit_url = url + "?$limit={0}&$page={1}".format(limit, i)
      r = send_request("GET", self.pc_ip, limit_url)
      n_out = r.json()

      if n_out["$dataItemDiscriminator"] == "EMPTY_LIST":
        continue

      if out:
        out["data"].extend(n_out["data"]) 
      else:
        out = n_out
    #out = r.json()
    return out

  def get_name_uuid_map(self, cluster_uuid=None):
    vg_name_uuid_map = dict()
    out = self.list_all()
    if not out:
      return vg_name_uuid_map
    if "data" not in out.keys():
      return vg_name_uuid_map
    for i in out["data"]:
      if cluster_uuid:
        if i["clusterReference"] != cluster_uuid:
          continue
      vg_name_uuid_map[i["name"]] = i["extId"]
    return vg_name_uuid_map

  def get_uuid_name_map(self):
    vg_name_uuid_map = self.get_name_uuid_map()
    vg_uuid_name_map = dict(zip(vg_name_uuid_map.values(), vg_name_uuid_map.keys()))
    return vg_uuid_name_map

  def get(self, vg_name=None, vg_uuid=None):
    if vg_uuid:
      url = "api/storage/{0}/config/volume-groups/{1}".format(VG_API_VERSION, vg_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()["data"]
    else:
      out = self.list_all()
      if out["$dataItemDiscriminator"] == "EMPTY_LIST":
        print "There are no VG on this PC."
        return None
      for i in out["data"]:
        if i["name"] == vg_name:
          spec = i
          vg_uuid = i["extId"]
          break
      else:
        print "VG not found"
        return
    v = VG(self.pc_ip, uuid=vg_uuid, spec=spec, name=spec["name"])
    self.uuid = vg_uuid
    v.iscsi_target = spec["iscsiTargetName"]
    v.cluster = spec["clusterReference"]
    v.category_list = self.get_categories()
    #v.disk_list = self.get_disks()
    v.iscsi_attachment_list = self.get_iscsi_attachments()
    #v.hyp_attachment_list = self.get_hyp_attachments()
    v.is_chap_enabled = None
    if "enabledAuthentications" in spec.keys():
      v.is_chap_enabled = True
    return v

  def get_etag_header(self, vg_uuid):
    url = "api/storage/{0}/config/volume-groups/{1}".format(VG_API_VERSION, vg_uuid)
    r = send_request("GET", self.pc_ip, url)
    etag = None
    if "Etag" in r.headers:
      etag = r.headers["Etag"]
    return etag

  # Disk ops
  def add_disk(self, disk_size=None, ctr_uuid=None, disk_spec=None):
    url = "api/storage/{0}/config/volume-groups/{1}/disks".format(VG_API_VERSION, self.uuid)
    r = send_request("POST", self.pc_ip, url, json=disk_spec)
    out = r.json()
    

  def remove_disk(self, disk_uuid):
    url = "api/storage/{0}/config/volume-groups/{1}/disks/{2}".format(VG_API_VERSION, self.uuid, disk_uuid)
    r = send_request("DELETE", self.pc_ip, url)
    print r.status_code

  def update_disk(self):
    pass

  def get_disks(self):
    url = "api/storage/{0}/config/volume-groups/{1}/disks".format(VG_API_VERSION, self.uuid)
    r = send_request("GET", self.pc_ip, url)
    spec = r.json()
    disk_list = list()
    if spec["$dataItemDiscriminator"] == "EMPTY_LIST":
      return []
    for disk in spec["data"]:
      disk.pop("$reserved")
      disk.pop("$objectType")
      disk.pop("links")
      disk_list.append(disk)
    return disk_list

  # Category ops
  def add_category(self, cat_key=None, cat_val=None, cat_uuid=None):
    if not cat_uuid:
      c = Category(self.pc_ip)
      c1 = c.get(cat_key, cat_val)
      cat_uuid = c1.uuid
      print "Adding category: ({0}, {1}), uuid: {2} to VG: {3}, {4}".format(cat_key, cat_val, cat_uuid, self.name, self.uuid)
    else:
      print "Adding category: uuid: {0} to VG: {1}, {2}".format(cat_uuid, self.name, self.uuid)
    url = "api/storage/{0}/config/volume-groups/{1}/$actions/associate-category".format(VG_API_VERSION, self.uuid)
    body = {"categories": [{"entityType": "CATEGORY","extId":cat_uuid}]}
    #print body
    r = send_request("POST", self.pc_ip, url, json=body)
    print r.status_code, r.text
    print body
    #out = r.json()
    #print r.status_code, out 

  def remove_category(self, cat_key=None, cat_val=None, cat_uuid=None):
    if not cat_uuid:
      c = Category(self.pc_ip)
      c1 = c.get(cat_key, cat_val)
      cat_uuid = c1.uuid
      print "Removing category: ({0}, {1}), uuid: {2} to VG: {3}, {4}".format(cat_key, cat_val, cat_uuid, self.name, self.uuid)
    else:
      print "Removing category: uuid: {0} to VG: {1}, {2}".format(cat_uuid, self.name, self.uuid)
    url = "api/storage/{0}/config/volume-groups/{1}/$actions/disassociate-category".format(VG_API_VERSION, self.uuid)
    body = {"categories": [{"entityType": "CATEGORY","extId":cat_uuid}]}
    r = send_request("POST", self.pc_ip, url, json=body)
    print r.status_code, r.text
    print body
    pass

  def get_categories(self):
    url = "api/storage/{0}/config/volume-groups/{1}/category-associations".format(VG_API_VERSION, self.uuid)
    r = send_request("GET", self.pc_ip, url)
    #print r.status_code, r.text
    spec = r.json()
    category_list = list()
    if spec["$dataItemDiscriminator"] == "EMPTY_LIST":
      return []
    #print spec["data"]
    for category in spec["data"]:
      category.pop("$reserved")
      category.pop("$objectType")
      category_list.append(category)
    return category_list

  # Iscsi ops
  def get_iscsi_attachments(self):
    url = "api/storage/{0}/config/volume-groups/{1}/iscsi-client-attachments".format(VG_API_VERSION, self.uuid)
    r = send_request("GET", self.pc_ip, url)
    spec = r.json()
    iscsi_client_list = list()
    if spec["$dataItemDiscriminator"] == "EMPTY_LIST":
      return []
    for iscsi_client in spec["data"]:
      iscsi_client.pop("$reserved")
      iscsi_client.pop("$objectType")
      iscsi_client_list.append(iscsi_client)
    return iscsi_client_list

  def attach_iscsi(self, vg_attach_spec):
    etag = None
    if VG_ETAG_REQUIRED:
      etag = self.get_etag_header(self.uuid)
    # Sample vg_attach_spec, {"iscsiInitiatorName": "iqn.1994-05.com.redhat:6582509746c4"}
    url = "api/storage/{0}/config/volume-groups/{1}/$actions/attach-iscsi-client".format(VG_API_VERSION, self.uuid)
    r = send_request("POST", self.pc_ip, url, json=vg_attach_spec, etag=etag)
    out = r.json()
    print out
    return out["metadata"]["links"][0]["href"]

  def detach_iscsi(self, iscsi_client_id):
    etag = None
    if VG_ETAG_REQUIRED:
      etag = self.get_etag_header(self.uuid)
    url = "api/storage/{0}/config/volume-groups/{1}/$actions/detach-iscsi-client/{2}".format(VG_API_VERSION, self.uuid, iscsi_client_id)
    r = send_request("POST", self.pc_ip, url, etag=etag)
    out = r.json()
    return out["metadata"]["links"][0]["href"]

  # Hypervisor attachement ops
  def get_hyp_attachments(self):
    url = "api/storage/{0}/config/volume-groups/{1}/vm-attachments".format(VG_API_VERSION, self.uuid)
    r = send_request("GET", self.pc_ip, url)
    spec = r.json()
    hyp_client_list = list()
    if spec["$dataItemDiscriminator"] == "EMPTY_LIST":
      return []
    for hyp_client in spec["data"]:
      hyp_client.pop("$reserved")
      hyp_client.pop("$objectType")
      hyp_client_list.append(hyp_client)
    return hyp_client_list

  def attach_vm(self):
    pass

  def detach_vm(self):
    pass

  # Migrate ops
  def migrate(self):
    pass

  def remove_chap(self):
    etag = None
    if VG_ETAG_REQUIRED:
      etag = self.get_etag_header(self.uuid)
    url = "api/storage/{0}/config/volume-groups/{1}".format(VG_API_VERSION, self.uuid)
    spec = {"extId": self.uuid,"sharingStatus":"SHARED","enabledAuthentications":"NONE"}
    r = send_request("PATCH", self.pc_ip, url, json=spec, etag=etag) 
    print r.status_code

  def add_chap(self, chap_password):
    etag = None
    if VG_ETAG_REQUIRED:
      etag = self.get_etag_header(self.uuid)
    url = "api/storage/{0}/config/volume-groups/{1}".format(VG_API_VERSION, self.uuid)
    spec = {"extId": self.uuid,"sharingStatus":"SHARED", "targetSecret":chap_password,"enabledAuthentications":"CHAP"}
    r = send_request("PATCH", self.pc_ip, url, json=spec, etag=etag) 
    print r.status_code
    out = r.json()
    print out["metadata"]["links"][0]["href"]

  def create_recovery_point(self, rpt_name=None):
    if not rpt_name:
      rpt_name = "{0}-rec-point-{1}".format(self.name, datetime.datetime.now().strftime("%Y%m%d-%H%M%S"))
    payload = {"name": rpt_name, "recoveryPointType": "APPLICATION_CONSISTENT", "volumeGroupReferenceList": [self.uuid]} 
    url = "api/dataprotection/v4.0.a1/config/recovery-points"
    r = send_request("POST", self.pc_ip, url, json=payload)
    if r.status_code == 201:
      out = r.json()
      print "Recovery Point created successfully, extID: {0}\n".format(out["data"]["extId"])
      return out["data"]["extId"]
    else:
      print "Recovery Point creation failed, with error: {0}\n".format(r.text)
      return None

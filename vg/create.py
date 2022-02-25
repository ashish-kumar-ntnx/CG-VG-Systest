from tinydb import TinyDB, Query
import time
import requests
import random
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass

CLUSTER_DB = TinyDB("../db/cluster.json")
CTR_DB = TinyDB("../db/ctr.json")
VG_DB = TinyDB("../db/vg.json")
#VG_PREFIX_1 = "vg-a-"
#VG_PREFIX_2 = "vg-b-"
#VG_PREFIX_LIST = ["vg-a-", "vg-b-"]
CLUSTER_LIST = ["PC-A-PE-1", "PC-A-PE-2"]
VG_PREFIX_CLUSTER_MAP = {"vg-a-": "PC-A-PE-1", "vg-b-": "PC-A-PE-2"}
VG_COUNT = 200
DISK_COUNT_RANGE = (10, 30)
PC_IP = "10.45.72.242"
AUTH = ("admin", "Nutanix.123")
CHAP_PASS_TARGET = "123456789012"
CHAP_PASS_CLIENT = "abcdefghijkl"

def create_vg():
  failed_vgs_dict = dict()
  vg_map = dict()
  for VG_PREFIX in VG_PREFIX_CLUSTER_MAP:
    cluster_name = VG_PREFIX_CLUSTER_MAP[VG_PREFIX]
    q = Query()
    cluster_id = CLUSTER_DB.search(q.name == cluster_name)[0]["uuid"]
    for i in range(1, VG_COUNT + 1):
      vg_name = VG_PREFIX + str(i)
      vg_spec = dict()
      vg_spec["name"] = vg_name
      vg_spec["description"] = "VG: {0} on Cluster: {1}".format(vg_name, cluster_name)
      vg_spec["sharingStatus"] = "SHARED"
      vg_spec["iscsiTargetPrefix"] = vg_name
      vg_spec["clusterReference"] = cluster_id
      #vg_spec["enabledAuthentications"] = "CHAP"
      #vg_spec["targetSecret"] = CHAP_PASS_TARGET

      print "Creating VG: {0} ...".format(vg_name)
      url = "https://{0}:9440/api/storage/v4.0.a1/config/volume-groups".format(PC_IP)
      r = requests.post(url, auth=AUTH, json=vg_spec, verify=False)
      out = r.json()
      task_url = out["metadata"]["links"][0]["href"]
      #extId = out["data"]["extId"]
      task_status, extId = check_tasks(task_url)
      if task_status:
        print "VG: {0}, Created Successfully.".format(vg_name)
      else:
        print "VG: {0}, Creation Failed.".format(vg_name)
        failed_vgs_dict[vg_name] = task_url
        continue

      tmp = dict()
      tmp["name"] = vg_name
      tmp["extId"] = extId
      tmp["disk_extId_list"] = add_disks(extId, cluster_id)      
      vg_map[vg_name] = tmp
      VG_DB.insert({"name": vg_name, "uuid": extId, "disk_extId_list": tmp["disk_extId_list"]})
      print "\n\n"
  print vg_map
  print failed_vgs_dict

def add_disks(extId, cluster_id):
  disk_extid_list = list()
  num_disks = random.randint(DISK_COUNT_RANGE[0], DISK_COUNT_RANGE[1])
  q = Query()
  ctr_list = CTR_DB.search(q.cluster_uuid == cluster_id)
  ctr_list = [i["uuid"] for i in ctr_list if i["name"].startswith("cg-vg-ctr-")]
  for i in range(num_disks):
    disk_size = random.randint(1, 3) * 1024 * 1024 *1024
    ctr_uuid = ctr_list[random.randint(0, len(ctr_list)-1)]
    print "\nAdding disk_num: {0} of size: {1} bytes, to VG: {2} from ctr: {3}".format(i + 1, disk_size, extId, ctr_uuid)
    disk_spec = dict()
    disk_spec["diskSizeBytes"] = disk_size
    disk_spec["diskDataSourceReference"] = dict()
    disk_spec["diskDataSourceReference"]["extId"] = ctr_uuid
    disk_spec["diskDataSourceReference"]["entityType"] = "STORAGE_CONTAINER"
    url = "https://{0}:9440/api/storage/v4.0.a1/config/volume-groups/{1}/disks".format(PC_IP, extId)
    #print url
    r = requests.post(url, auth=AUTH, json=disk_spec, verify=False)
    out = r.json()
    #print out
    disk_extid = out["data"]["extId"] 
    disk_extid_list.append({"disk_extid": disk_extid, "ctr_uuid": ctr_uuid})
  return disk_extid_list

def check_tasks(task_url):
  retry_count = 10
  while retry_count:
    r = requests.get(task_url, auth=AUTH, verify=False)
    out = r.json()
    try:
      if out["status"] == "SUCCEEDED":
        return True, out["entity_reference_list"][0]["uuid"]
    except:
      pass
    print "VG create task not SUCCEEDED yet, retrying..."
    time.sleep(2)
    retry_count -= 1
  return False, ""

if __name__=="__main__":
  create_vg()

from lib import *
import time

class RecoveryPlan(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.spec = spec
    self.name = name

  def create(self, spec):
    #rp_spec = {"spec": spec, "api_version": "3.1", "metadata": {"kind": "recovery_plan"}}
    #print spec
    url = "api/nutanix/v3/recovery_plans"
    r = send_request("POST", self.pc_ip, url, json=spec)
    out = r.json()
    #print out
    time.sleep(5)
    task_uuid = out["status"]["execution_context"]["task_uuid"]
    print task_uuid
    self.uuid = out["metadata"]["uuid"]
    self.name = spec["spec"]["name"]
    return self

  def remove(self):
    url = "api/nutanix/v3/recovery_plans/{0}".format(self.uuid)
    r = send_request("DELETE", self.pc_ip, url)
    print r.status_code

  def edit(self, spec):
    url = "api/nutanix/v3/recovery_plans/{0}".format(self.uuid)
    r = send_request("PUT", self.pc_ip, url, json=spec)
    print r.status_code

  def list_all(self):
    url = "api/nutanix/v3/recovery_plans/list"
    r = send_request("POST", self.pc_ip, url, json={})
    out = r.json()
    return out

  def get(self, rp_uuid=None, rp_name=None):
    if rp_uuid:
      url = "api/nutanix/v3/recovery_plans/{0}".format(rp_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()
    else:
      out = self.list_all()
      for i in out["entities"]:
        if i["spec"]["name"] == rp_name:
          spec = i
          rp_uuid = i["metadata"]["uuid"]
          break
      else:
        print "Recovery Plan not found"
        return
    r = RecoveryPlan(self.pc_ip, uuid=rp_uuid, spec=spec, name=spec["spec"]["name"])
    return r

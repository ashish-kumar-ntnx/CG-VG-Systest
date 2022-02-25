from lib import *
import time

class ProtectionRule(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.spec = spec
    self.name = name

  def create(self, spec):
    #rp_spec = {"spec": spec, "api_version": "3.1", "metadata": {"kind": "recovery_plan"}}
    #print spec
    url = "api/nutanix/v3/protection_rules"
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
    url = "api/nutanix/v3/protection_rules/{0}".format(self.uuid)
    r = send_request("DELETE", self.pc_ip, url)
    print r.status_code

  def list_all(self, filter_criteria=None):
    url = "api/nutanix/v3/protection_rules/list"
    payload = dict()
    if filter_criteria:
      payload = filter_criteria
    r = send_request("POST", self.pc_ip, url, json=payload)
    out = r.json()
    return out

  def get(self, pr_uuid=None, pr_name=None):
    if pr_uuid:
      url = "api/nutanix/v3/protection_rules/{0}".format(pr_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()
    if pr_name:
      filter_criteria = {"filter":"name=={0}".format(pr_name)}
      out = self.list_all(filter_criteria=filter_criteria)
      spec = out["entities"][0]
      #print spec
      if spec:
        pr_uuid = spec["metadata"]["uuid"]
      else:
        print "Protection Rule not found"
        return
    r = ProtectionRule(self.pc_ip, uuid=pr_uuid, spec=spec, name=spec["spec"]["name"])
    return r

  def update(self, spec):
    #print spec
    url = "api/nutanix/v3/protection_rules/{0}".format(self.uuid)
    #print url
    r = send_request("PUT", self.pc_ip, url, json=spec)
    #out = r.json()
    #time.sleep(1)
    print r.status_code

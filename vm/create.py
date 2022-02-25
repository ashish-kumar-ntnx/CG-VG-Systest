from tinydb import TinyDB, Query
import time
import requests
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass


BATCH = 10
PC_IP = "10.45.72.242"
AUTH = ("admin", "Nutanix.123")
db = TinyDB("../db/vm_extended_spec.json")

def check_tasks(task):
  url = "https://{0}:9440/api/nutanix/v3/tasks/{1}".format(PC_IP, task)
  retry_count = 10
  while retry_count:
    r = requests.get(url, auth=AUTH, verify=False)
    out = r.json()
    if out["status"] == "SUCCEEDED":
      return True
    print "VM create task not SUCCEEDED yet, retrying..."
    time.sleep(2)
    retry_count -= 1
  return False

def create_vm():
  task_list = list()
  vm_table = db.table()
  failed_vms_dict = dict()
  for i in vm_table.all():
    vm_name = i["name"]
    vm_spec = i["spec"]
    print "Creating VM: {0} ...".format(vm_name)
    url = "https://{0}:9440/api/nutanix/v3/vms".format(PC_IP)
    r = requests.post(url, auth=AUTH, json=vm_spec, verify=False)
    out = r.json()
    task = out["status"]["execution_context"]["task_uuid"]
    task_status = check_tasks(task)
    if task_status:
      print "VM: {0}, Created Successfully.".format(vm_name)
    else:
      print "VM: {0}, Creation Failed.".format(vm_name)
      failed_vms_dict[vm_name] = out["metadata"]["uuid"]
    print "\n"
  return failed_vms_dict

if __name__=="__main__":
  failed_vms_dict = create_vm() 
  print failed_vms_dict

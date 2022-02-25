from lib import *
from framework.cluster_entity import Cluster
import paramiko
import warnings
warnings.filterwarnings(action='ignore',module='.*paramiko.*')

class VM(object):
  def __init__(self, pc_ip, uuid=None, spec=None, name=None):
    self.pc_ip = pc_ip
    self.uuid = uuid
    self.spec = spec
    self.name = name
    self.cluster_name = None
    self.cluster_uuid = None

  def create(self, vm_spec):
    url = "api/nutanix/v3/vms"
    r = send_request("POST", self.pc_ip, url, json=vm_spec)
    out = r.json()
    return out["status"]["execution_context"]["task_uuid"]

  def remove(self):
    print "Deleting VM: {0} !!!".format(self.name)
    url = "api/nutanix/v3/vms/{0}".format(self.uuid)
    r = send_request("DELETE", self.pc_ip, url)
    print "Delete API status_code: {0}\n".format(r.status_code)

  def list_all(self):
    url = "api/nutanix/v3/vms/list"
    length = 20
    offset = 0
    r = send_request("POST", self.pc_ip, url, json={})
    out = r.json()
    total_matches = out["metadata"]["total_matches"]
    #print total_matches
    if total_matches > length:
      remaining = total_matches - length
    else:
      remaining = total_matches
    while remaining:
      offset += 20
      if remaining > 20:
        length = 20
      else:
        length = remaining
      payload = {"kind": "vm", "offset":offset, "length": length}
      remaining = remaining - length
      r = send_request("POST", self.pc_ip, url, json=payload)
      #print r.status_code, r.text
      o = r.json()
      out["entities"].extend(o["entities"])
    return out

  def get_name_uuid_map(self):
    vm_name_uuid_map = dict()
    out = self.list_all()
    for i in out["entities"]:
      vm_name_uuid_map[i["status"]["name"]] = i["metadata"]["uuid"]
    return vm_name_uuid_map

  def get_uuid_name_map(self):
    vm_name_uuid_map = self.get_name_uuid_map()
    vm_uuid_name_map = dict(zip(vm_name_uuid_map.values(), vm_name_uuid_map.keys()))
    return vm_uuid_name_map

  def get_vm_ip(self):
    if hasattr(self, "vm_ip"):
      return self.vm_ip
    body = {"entity_type":"vm","filter_criteria":"_entity_id_=={0}".format(self.uuid),"group_member_attributes":[{"attribute":"ip_addresses"}]}
    url = "api/nutanix/v3/groups"
    r = send_request("POST", self.pc_ip, url, json=body)
    out = r.json()
    try:
      self.vm_ip = out["group_results"][0]["entity_results"][0]["data"][0]["values"][0]["values"][0]
      return self.vm_ip
    except:
      return None

  #def execute(self, cmd, username="root", password="nutanix/4u"):
  def execute(self, cmd, username="nutanix", password="nutanix/4u"):
    self.vm_ip = self.get_vm_ip()
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=self.vm_ip, username=username, password=password)
    stdin,stdout,stderr = ssh_client.exec_command(cmd)
    out, err = stdout.read(), stderr.read()
    if err:
      print "CMD: {0} failed with error: {1}".format(cmd, err)
      return False, err
    return True, out

  def get(self, vm_uuid=None, vm_name=None, cluster_name=None):
    if vm_uuid:
      url = "api/nutanix/v3/vms/{0}".format(vm_uuid)
      r = send_request("GET", self.pc_ip, url)
      spec = r.json()
    else:
      url = "api/nutanix/v3/vms/list"
      filter_criteria = {"filter": "vm_name=={0}".format(vm_name)}
      r = send_request("POST", self.pc_ip, url, json=filter_criteria)
      out = r.json()
      for i in out["entities"]:
        if i["spec"]["name"] == vm_name and i["spec"]["cluster_reference"]["name"] == cluster_name:
          spec = i
          vm_uuid = i["metadata"]["uuid"]
          break
      else:
        print "VM not found"
        return
    v = VM(self.pc_ip, uuid=vm_uuid, spec=spec, name=spec["spec"]["name"])
    v.cluster_name = spec["spec"]["cluster_reference"]["name"]
    v.cluster_uuid = spec["spec"]["cluster_reference"]["uuid"]
    print "VM object created for VM: {0}, {1}".format(v.name, v.uuid)
    return v

  def get_json(self):
    url = "api/nutanix/v3/vms/{0}".format(self.uuid) 
    r = send_request("GET", self.pc_ip, url)
    return r.json()

  def update(self, vm_spec):
    url = "api/nutanix/v3/vms/{0}".format(self.uuid)
    r = send_request("PUT", self.pc_ip, url, json=vm_spec)
    out = r.json()
    return out["status"]["execution_context"]["task_uuid"]

  def migrate(self):
    pass

  def create_recovery_point(self):
    pass

  # Category ops
  def attach_category(self, cat_key, cat_val):
    vm_spec = self.get_json()
    vm_spec.pop("status")
    vm_spec["metadata"]["use_categories_mapping"] = True
    vm_spec["metadata"]["categories_mapping"] = {cat_key: [cat_val]}
    url = "api/nutanix/v3/vms/{0}".format(self.uuid)
    r = send_request("PUT", self.pc_ip, url, json=vm_spec)
    return r.json()

  def remove_category(self):
    #print "In remove_category"
    vm_spec = self.get_json()
    vm_spec.pop("status")
    vm_spec["metadata"]["use_categories_mapping"] = True
    vm_spec["metadata"]["categories_mapping"] = {}
    #vm_spec["metadata"]["categories"] = {}
    url = "api/nutanix/v3/vms/{0}".format(self.uuid)
    #print url, vm_spec
    r = send_request("PUT", self.pc_ip, url, json=vm_spec)
    return r.json()


  def get_categories(self):
    return self.spec["metadata"]["categories_mapping"]

  # Disk ops
  def add_disks(self):
    pass

  def get_disks(self):
    pass

  def remove_disk(self):
    pass

  # Nic ops
  def add_nics(self):
    pass

  def get_nics(self):
    pass

  def remove_nic(self):
    pass

  # Iscsi ops
  def enable_iscsi(self, os="rhel"):
    if os == "rhel":
      if not self.iscsi_enabled():
        cmd = "sudo yum install iscsi-initiator-utils -y"
        self.execute(cmd)
        cmd = "sudo systemctl enable iscsid; sudo systemctl start iscsid"
        self.execute(cmd)
        cmd = "sudo systemctl restart iscsid"
        self.execute(cmd)
        print "iscsi enabled successfully."
      else:
        print "iscsi already enabled."

  def iscsi_enabled(self):
    cmd = "systemctl is-active iscsid"
    #cmd = "systemctl is-active --quiet iscsid"
    cmd_success, out = self.execute(cmd)
    #print out
    #if cmd_success:
    if out.strip("\n") != "unknown":
      return True
    return False
    
  def iscsi_target_login(self, dsip=None, iscsi_port=3260, target_chap_secret=None, client_chap_secret=None):
    if not dsip:
      cluster_uuid = self.cluster_uuid 
      Clus = Cluster(self.pc_ip)
      c = Clus.get(cluster_uuid=self.cluster_uuid)
      dsip = c.get_dsip()
    #cmd = "sudo /usr/sbin/iscsiadm -m discovery -t st -p {0}:{1}".format(dsip, iscsi_port)
    if not target_chap_secret:
      cmd = "for disk in `sudo /usr/sbin/iscsiadm -m discovery -t st -p %s:%s |awk '{print $2}'`; do sudo /usr/sbin/iscsiadm -m node --targetname $disk --portal %s:%s --login; done" %(dsip, iscsi_port, dsip, iscsi_port)
    else:
      cmd = "for disk in `sudo /usr/sbin/iscsiadm -m discovery -t st -p %s:%s |awk '{print $2}'`; do sudo /usr/sbin/iscsiadm -m node --targetname $disk -o update -n node.session.auth.password -v %s; sudo /usr/sbin/iscsiadm -m node --targetname $disk --portal %s:%s --login; done" %(dsip, iscsi_port, target_chap_secret, dsip, iscsi_port)
    print cmd
    _, out = self.execute(cmd)
    print out    

  def get_sd_disk_list(self):
    cmd = "sudo fdisk -l |grep '^Disk /dev/sd' |grep -v 'sda:' |awk '{print $2}' | awk -F [:] '{print $1}' |xargs"
    _, out = self.execute(cmd)
    #print out
    return out

  def iscsi_get_logged_in_targets(self, dsip=None, iscsi_port=3260):
    pass 

  def get_iqn(self):
    if hasattr(self, "iqn"):
      return self.iqn
    cmd = "cat /etc/iscsi/initiatorname.iscsi"
    _, out = self.execute(cmd)
    #print out
    iqn = out.strip("\n").split("=")[-1]
    self.iqn = iqn
    return self.iqn

  def generate_new_iqn(self):
    cmd = 'echo "InitiatorName=`/sbin/iscsi-iname`" | sudo tee /etc/iscsi/initiatorname.iscsi'
    _, out = self.execute(cmd)
    iqn = out.strip("\n").split("=")[1]
    self.iqn = iqn
    print "Generated new iqn: {0} for VM: {1}".format(self.iqn, self.name)
    return self.iqn

  def iscsi_target_logout(self, dsip=None, iscsi_port=3260):
    if not dsip:
      cluster_uuid = self.cluster_uuid 
      Clus = Cluster(self.pc_ip)
      c = Clus.get(cluster_uuid=self.cluster_uuid)
      dsip = c.get_dsip()
    #cmd = "sudo /usr/sbin/iscsiadm -m discovery -t st -p {0}:{1}".format(dsip, iscsi_port)
    #cmd = "for disk in `sudo /usr/sbin/iscsiadm -m discovery -t st -p %s:%s |awk '{print $2}'`; do sudo /usr/sbin/iscsiadm -m node --targetname $disk --portal %s:%s -u; done" %(dsip, iscsi_port, dsip, iscsi_port)
    cmd = "sudo /usr/sbin/iscsiadm --mode node --logoutall=all"
    _, out = self.execute(cmd)
    cmd = "for disk in `sudo /usr/sbin/iscsiadm -m discovery -t st -p %s:%s |awk '{print $2}'`; do sudo /usr/sbin/iscsiadm -m node --targetname $disk --portal %s:%s --logout; done" %(dsip, iscsi_port, dsip, iscsi_port)
    print cmd
    _, out = self.execute(cmd)
    print out    

  # NGT ops
  def enable_ngt(self):
    pass

  def get_ngt_status(self):
    pass

  # IO ops
  def enable_fio(self):
    pass

  def format_disks(self):
    pass

  def mount_disks(self):
    pass

  def trigger_fio(self):
    cmd = "wget http://uranus.corp.nutanix.com/~ashish.kumar/fio.sh; sudo chmod +x ~/fio.sh; nohup sudo ./fio.sh &"
    #cmd = "wget http://filer.dev.eng.nutanix.com:8080/Users/ashish.kumar/fio.sh; sudo chmod +x ~/fio.sh; nohup sudo ./fio.sh &"
    _, out = self.execute(cmd)
    print out

  def enable_vdbench(self):
    cmd = "sudo yum install unzip java -y"
    print "Installing dependent libs for vdbench"
    self.execute(cmd)
    print "Downloading setup_vdbench50407.sh file to VM: {0}".format(self.name)
    #cmd = "curl -O http://filer.dev.eng.nutanix.com:8080/Users/ashish.kumar/vdbench_files/setup_vdbench50407.sh"
    cmd = "curl -O http://uranus.corp.nutanix.com/~ashish.kumar/setup_vdbench50407.sh"
    self.execute(cmd)
    print "Running vdbench setup script."
    cmd = "chmod +x /home/nutanix/setup_vdbench50407.sh; /home/nutanix/setup_vdbench50407.sh"
    self.execute(cmd)

  def trigger_vdbench(self):
    pass

  def set_vdbench_iorate(self):
    pass

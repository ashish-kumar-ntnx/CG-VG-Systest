import time
from pprint import pprint
from vg_spec_generator import generate_vg_spec
from framework.vg_entity import VG

vg_spec = generate_vg_spec()
#pprint(vg_spec)
PC_IP = "10.40.216.116"
vg_obj = VG(PC_IP)
for vg_name in vg_spec:
  print "Creating VG: {0}".format(vg_name)
  spec = vg_spec[vg_name]["spec"]
  disk_list = vg_spec[vg_name]["disk_list"]
  task_url = vg_obj.create(vg_spec=spec)
  vg_spec[vg_name]["task_url"] = task_url
  time.sleep(2)
  vg = vg_obj.get(vg_name=vg_name)
  vg_uuid = vg.uuid
  print "Adding disks to the {0} - {1}".format(vg_name, vg_uuid)
  for disk_spec in disk_list:
    vg.add_disk(disk_spec=disk_spec)

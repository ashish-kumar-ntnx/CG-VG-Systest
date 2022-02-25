import time
import requests
try:
  from requests.exceptions import ConnectionError, ReadTimeout
  from requests.packages.urllib3 import disable_warnings
  disable_warnings()
except Exception:
  pass


#{"action_on_failure":"CONTINUE","execution_order":"NON_SEQUENTIAL","api_request_list":[{"operation":"POST","path_and_params":"/api/nutanix/v3/images","body":{"spec":{"name":"win2019_server","resources":{"image_type":"DISK_IMAGE","source_uri":"http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/win2019_server_standard.qcow2"}},"metadata":{"kind":"image"},"api_version":"3.1.0"}}],"api_version":"3.0"}

AUTH = ("admin", "Nutanix.123")
#PC_IP = "127.0.0.1"
PC_IP = "10.45.72.182"

body = {"spec":{"name":"win2019_server","resources":{"image_type":"DISK_IMAGE","source_uri":"http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/win2019_server_standard.qcow2"}},"metadata":{"kind":"image"},"api_version":"3.1.0"}

image_urls = {
  "win2019_server": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/win2019_server_standard.qcow2",
  "win2016_server": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/win2016_standard_vdisk.qcow2",
  "win2012r2_server": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/win2012r2_standard_vdisk.qcow2",
  "win2008r2_server": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/win2008r2_standard_vdisk.qcow2",
  "rhel_77": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel-server-7.7-x86_64_vdisk.qcow2",
  "rhel_76": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel-server-7.6-x86_64_vdisk.qcow2",
  "rhel_74": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel74_vdisk.qcow2",
  "rhel_73": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel73_vdisk.qcow2",
  "rhel_72": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel72_vdisk.qcow2",
  "rhel_69": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel69_vdisk.qcow2",
  "rhel_68": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel68_vdisk.qcow2",
  "rhel_67": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/rhel67_vdisk.qcow2",
  "oel_69": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/oel69_vdisk.qcow2",
  "oel_77": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/oel77_vdisk.qcow2",
  "centos_72": "http://endor.dyn.nutanix.com/GoldImages/draas_static_ip_ngt/CentOS_7_2_NGT_static_ip.qcow2",
  "sles11_sp4": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/sles11_sp4_vdisk.qcow2",
  "sles12_sp4": "http://endor.dyn.nutanix.com/acro_images/automation/ahv_guest_os/DSK/sles12_sp4_vdisk.qcow2"
}

for image in image_urls:
  print "Image: {0}".format(image)
  url = "https://{0}:9440/api/nutanix/v3/images".format(PC_IP)
  body["spec"]["name"] = image
  body["spec"]["resources"]["source_uri"] = image_urls[image]
  r = requests.post(url, auth=AUTH, json=body, verify=False)
  out = r.json()
  print "For Image: {0}, Task UUID: {1}".format(image, out["status"]["execution_context"]["task_uuid"])
  time.sleep(0.2)

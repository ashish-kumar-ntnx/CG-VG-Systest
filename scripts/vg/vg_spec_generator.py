import random
from pprint import pprint

def generate_vg_spec():
  vg_prefix = "ak-vg-"
  num_vg = 20
  ctr_list = ["cg-vg-ctr-1", "cg-vg-ctr-2"]
  ctr_uuid_list = ["866adfd2-eab8-415f-9f3b-1976af859feb", "b4f2918f-617a-473d-bd7f-ea677a19df27"]
  disk_count_per_vg = [10, 30]
  disk_size_range = [1, 3]
  vg_password = "Nutanix.1234"
  cluster_name = "SOURCE-PE"
  cluster_uuid = "0005c4c8-690a-f132-0000-000000028b6b"

  vg_spec = dict()
  for i in range(13, num_vg + 1):
    vg_name = vg_prefix + str(i)
    vg_desc = "Creating VG: {0}".format(vg_name)
    vg_spec[vg_name] = dict()
    tmp = dict()
    tmp["name"] = vg_name
    tmp["description"] = vg_desc
    tmp["sharingStatus"] = "SHARED"
    tmp["iscsiTargetPrefix"] = vg_name
    tmp["targetSecret"] = vg_password
    tmp["enabledAuthentications"] = "CHAP"
    tmp["clusterReference"] = cluster_uuid
    vg_spec[vg_name]["spec"] = tmp
    vg_spec[vg_name]["disk_list"] = list()
    disk_count = random.randint(disk_count_per_vg[0], disk_count_per_vg[1])
    for i in range(disk_count):
      tmp = dict()
      ctr_uuid = ctr_uuid_list[random.randint(0,1)]
      disk_size = random.randint(disk_size_range[0], disk_size_range[1])
      tmp["diskSizeBytes"] = disk_size * 1024 * 1024 * 1024
      tmp["diskDataSourceReference"] = {"extId": ctr_uuid, "entityType": "STORAGE_CONTAINER"}
      vg_spec[vg_name]["disk_list"].append(tmp)

  return vg_spec
